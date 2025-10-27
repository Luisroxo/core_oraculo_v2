from selenium.common.exceptions import TimeoutException, WebDriverException
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import sys
import os
from dotenv import load_dotenv

import logging_config
import logging
import db

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'), override=True)

def fetch_kommo_articles():
	def _extract_article_details(driver, url_art, categoria):
		try:
			driver.get(url_art)
			WebDriverWait(driver, 15).until(
				EC.presence_of_element_located((By.CLASS_NAME, "blog-article__content"))
			)
			art_soup = BeautifulSoup(driver.page_source, "html.parser")
			title = art_soup.find(['h1', 'h2']).get_text(strip=True) if art_soup.find(['h1', 'h2']) else ''
			content_div = art_soup.find('div', class_='blog-article__content')
			content = content_div.get_text("\n", strip=True) if content_div else ''
			if title.strip().lower() == 'faça login' or not content.strip():
				logging.warning(f"Ignorado: {url_art} - título '{title}' ou conteúdo vazio.")
				return None
			pub_date = ''
			time_tag = art_soup.find('time')
			if time_tag:
				pub_date = time_tag.get_text(strip=True)
			else:
				date_div = art_soup.find('div', string=lambda t: t and 'de' in t and '202' in t)
				if date_div:
					pub_date = date_div.get_text(strip=True)
			# Seletores mais robustos para metadados
			reading_time = ''
			views = None
			reading_span = art_soup.find('span', string=lambda t: t and 'min.' in t)
			if reading_span:
				reading_time = reading_span.get_text(strip=True)
			views_span = art_soup.find('span', string=lambda t: t and t.isdigit())
			if views_span:
				views = int(views_span.get_text(strip=True))
			author = ''
			author_tag = art_soup.find('a', href=True, string=True)
			if author_tag:
				author = author_tag.get_text(strip=True)
			summary = ''
			summary_div = art_soup.find('div', class_='blog-article__toc')
			if summary_div:
				summary = summary_div.get_text("\n", strip=True)
			faq = []
			faq_items = art_soup.find_all('div', class_='faq__item')
			for item in faq_items:
				q = item.find(['h3', 'h4'])
				a = item.find('p')
				if q and a:
					faq.append({'question': q.get_text(strip=True), 'answer': a.get_text(strip=True)})
			return {
				'title': title,
				'url': url_art,
				'content': content,
				'published_at': pub_date,
				'reading_time': reading_time,
				'views': views,
				'author': author,
				'summary': summary,
				'faq': faq,
				'categoria': categoria
			}
		except TimeoutException:
			logging.warning(f"Timeout ao coletar artigo {url_art}")
			return None
		except WebDriverException as e:
			logging.warning(f"WebDriverException ao coletar artigo {url_art}: {e}")
			return None
		except Exception as e:
			logging.warning(f"Erro inesperado ao coletar artigo {url_art}: {e}")
			return None
	chrome_options = Options()
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--window-size=1920,1080')
	chrome_options.add_argument('--ignore-certificate-errors')
	chrome_options.add_argument('--allow-insecure-localhost')
	chrome_options.add_argument('--ignore-ssl-errors=true')
	chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')
	driver = uc.Chrome(options=chrome_options, driver_executable_path=r'C:\ChromeDriver\chromedriver-win64\chromedriver.exe')

	url = "https://www.kommo.com/br/blog/"
	logging.info(f"Acessando {url}")
	driver.get(url)
	print("--- INÍCIO HTML DA PÁGINA PRINCIPAL ---")
	print(driver.page_source)
	print("--- FIM HTML DA PÁGINA PRINCIPAL ---")
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "a")))
	soup = BeautifulSoup(driver.page_source, "html.parser")
	articles = []
	categorias = set()
	# Coleta de categorias usando seletor CSS mais específico
	for cat_link in soup.select(".blog-categories__item a"):
		href = cat_link.get('href', '')
		texto = cat_link.get_text(strip=True)
		# Evita categorias genéricas e duplicadas
		if href.startswith('/br/blog/') and texto and 'todos' not in texto.lower() and 'all' not in href:
			categorias.add((texto, f"https://www.kommo.com{href}"))
	print("Categorias encontradas:")
	for nome_cat, url_cat in categorias:
		print(f"- {nome_cat}: {url_cat}")

	# Coletar artigos destacados usando cards
	print("Coletando artigos da seção 'Melhor do blog'...")
	artigos_melhor = set()
	for card in soup.select(".blog-articles__item a"):
		href = card.get('href', '')
		if href.startswith('/br/blog/') and not href.endswith('/') and '?' not in href:
			artigos_melhor.add(f'https://www.kommo.com{href}')
	for url_art in artigos_melhor:
		artigo = _extract_article_details(driver, url_art, 'Melhor do blog')
		if artigo:
			articles.append(artigo)

	# Continua processamento dos artigos por categoria usando seletor CSS específico
	for nome_cat, url_cat in categorias:
		logging.info(f"Acessando categoria: {nome_cat} - {url_cat}")
		try:
			driver.get(url_cat)
			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "blog-articles__item")))
			soup_cat = BeautifulSoup(driver.page_source, "html.parser")
			links = set()
			for card in soup_cat.select(".blog-articles__item a"):
				href = card.get('href', '')
				if href.startswith('/br/blog/') and not href.endswith('/') and '?' not in href:
					links.add(f'https://www.kommo.com{href}')
			for url_art in links:
				artigo = _extract_article_details(driver, url_art, nome_cat)
				if artigo:
					articles.append(artigo)
		except TimeoutException:
			logging.warning(f"Timeout ao acessar categoria {url_cat}")
		except WebDriverException as e:
			logging.warning(f"WebDriverException ao acessar categoria {url_cat}: {e}")
		except Exception as e:
			logging.warning(f"Erro inesperado ao acessar categoria {url_cat}: {e}")
	driver.quit()
	logging.info(f"Encontrados {len(articles)} artigos no Kommo.")
	return articles

def fetch_bling_articles():
	chrome_options = Options()
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--window-size=1920,1080')
	chrome_options.add_argument('--ignore-certificate-errors')
	chrome_options.add_argument('--allow-insecure-localhost')
	chrome_options.add_argument('--ignore-ssl-errors=true')
	chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')
	driver = uc.Chrome(options=chrome_options, driver_executable_path=r'C:\ChromeDriver\chromedriver-win64\chromedriver.exe')
	url = "https://blog.bling.com.br/"
	logging.info(f"Acessando {url}")
	driver.get(url)
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "article")))
	soup = BeautifulSoup(driver.page_source, "html.parser")
	articles = []
	for post in soup.find_all('article'):
		title_tag = post.find(['h1', 'h2', 'h3', 'h4'])
		link_tag = post.find('a', href=True)
		if title_tag and link_tag:
			title = title_tag.get_text(strip=True)
			href = link_tag['href']
			if title and href:
				artigo = None
				try:
					driver.get(href)
					WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
					art_soup = BeautifulSoup(driver.page_source, "html.parser")
					content = ''
					content_div = art_soup.find('div', class_='post-content')
					if content_div:
						content = content_div.get_text("\n", strip=True)
					pub_date = ''
					time_tag = art_soup.find('time')
					if time_tag:
						pub_date = time_tag.get_text(strip=True)
					author = ''
					author_tag = art_soup.find('a', href=True, string=True)
					if author_tag:
						author = author_tag.get_text(strip=True)
					artigo = {
						'title': title,
						'url': href,
						'content': content,
						'published_at': pub_date,
						'author': author,
						'categoria': 'Bling'
					}
				except Exception as e:
					logging.warning(f"Falha ao coletar artigo do Bling {href}: {e}")
				if artigo:
					articles.append(artigo)
	driver.quit()
	logging.info(f"Encontrados {len(articles)} artigos no Bling.")
	return articles

def main():
	fonte = sys.argv[1] if len(sys.argv) > 1 else 'kommo'
	if fonte == 'kommo':
		logging.info("Coletando artigos do blog Kommo...")
		articles = fetch_kommo_articles()
	elif fonte == 'bling':
		logging.info("Coletando artigos do blog Bling...")
		articles = fetch_bling_articles()
	else:
		logging.error("Fonte não reconhecida. Use 'kommo' ou 'bling'.")
		return
	for art in articles:
		logging.info(f"{art['title']} - {art['url']}")
	db.save_articles(articles, fonte)
	logging.info(f"{len(articles)} artigos salvos no banco de dados.")

if __name__ == "__main__":
	main()