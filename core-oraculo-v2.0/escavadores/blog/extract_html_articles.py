import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import logging

# Configuração básica do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def extract_articles_from_html():
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
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "a")))
    import time
    time.sleep(10)  # Aguarda 10 segundos para garantir carregamento dinâmico
    html_principal = driver.page_source
    print("\n--- INÍCIO HTML DA PÁGINA PRINCIPAL ---")
    print(html_principal[:10000])
    print("--- FIM HTML DA PÁGINA PRINCIPAL ---\n")
    soup = BeautifulSoup(html_principal, "html.parser")
    print("\n--- TODOS OS LINKS <a href> ENCONTRADOS ---")
    links_a = soup.find_all('a', href=True)
    for i, a in enumerate(links_a, 1):
        print(f"{i:02d}: {a['href']}")
    print("--- FIM DOS LINKS <a href> ---\n")
    articles = []
    # Busca todos os links de artigos diretamente na página principal
    links = set()
    for a in soup.find_all('a', href=True):
        href = a['href']
        # Ignora páginas de índice (como /noticias/ ou /blog/)
        if href.startswith('/br/blog/') and not href.rstrip('/').endswith(('noticias', 'blog')):
            links.add(f'https://www.kommo.com{href}')
    print(f"\n--- PRINT DEBUG ---\nTotal de links de artigos encontrados: {len(links)}\nLinks:")
    for i, link in enumerate(links, 1):
        print(f"{i:02d}: {link}")
    print("--- FIM PRINT DEBUG ---\n")
    print(f"\n--- PRINT DEBUG ---\nTotal de links de artigos encontrados: {len(links)}\nLinks:")
    for i, link in enumerate(links, 1):
        print(f"{i:02d}: {link}")
    print("--- FIM PRINT DEBUG ---\n")
    print(f"\n--- PRINT DEBUG ---\nTotal de links de artigos encontrados: {len(links)}\nLinks:")
    for i, link in enumerate(links, 1):
        print(f"{i:02d}: {link}")
    print("--- FIM PRINT DEBUG ---\n")
    # Diagnóstico: imprime HTML do primeiro artigo
    if links:
        print("\n--- INÍCIO HTML DO PRIMEIRO ARTIGO ---")
        try:
            driver.get(list(links)[0])
            import time
            time.sleep(10)
            print(driver.page_source)
        except Exception as e:
            print(f"Erro ao acessar o artigo: {e}")
        print("--- FIM HTML DO PRIMEIRO ARTIGO ---\n")
    for url_art in links:
        artigo = extract_article_details(driver, url_art)
        if artigo:
            articles.append(artigo)
    driver.quit()
    logging.info(f"Extraídos {len(articles)} artigos.")
    for art in articles:
        print(f"\n--- {art['title']} ---\nURL: {art['url']}\nAutor: {art['author']}\nData: {art['published_at']}\nResumo: {art['summary']}\nConteúdo: {art['content'][:300]}...\nFAQ: {art['faq']}")
    return articles

def extract_article_details(driver, url_art):
    try:
        driver.get(url_art)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "blog-article__content"))
        )
        art_soup = BeautifulSoup(driver.page_source, "html.parser")
        # Título
        title = ''
        if art_soup.find(['h1', 'h2']):
            title = art_soup.find(['h1', 'h2']).get_text(strip=True)
        elif art_soup.find('meta', property='og:title'):
            title = art_soup.find('meta', property='og:title').get('content', '')
        elif art_soup.find('meta', attrs={'name': 'title'}):
            title = art_soup.find('meta', attrs={'name': 'title'}).get('content', '')
        # Conteúdo
        content_div = art_soup.find('div', class_='blog-article__content')
        if content_div:
            content = content_div.get_text("\n", strip=True)
        else:
            content = '\n'.join([p.get_text(strip=True) for p in art_soup.find_all('p')])
        # Data
        pub_date = ''
        time_tag = art_soup.find('time')
        if time_tag:
            pub_date = time_tag.get_text(strip=True)
        elif art_soup.find('meta', attrs={'property': 'article:published_time'}):
            pub_date = art_soup.find('meta', attrs={'property': 'article:published_time'}).get('content', '')
        else:
            date_div = art_soup.find('div', string=lambda t: t and 'de' in t and '202' in t)
            if date_div:
                pub_date = date_div.get_text(strip=True)
        # Autor
        author = ''
        author_tag = art_soup.find('a', href=True, string=True)
        if author_tag:
            author = author_tag.get_text(strip=True)
        elif art_soup.find('meta', attrs={'name': 'author'}):
            author = art_soup.find('meta', attrs={'name': 'author'}).get('content', '')
        elif art_soup.find('span', class_='author'):
            author = art_soup.find('span', class_='author').get_text(strip=True)
        # Resumo
        summary = ''
        summary_div = art_soup.find('div', class_='blog-article__toc')
        if summary_div:
            summary = summary_div.get_text("\n", strip=True)
        elif art_soup.find('meta', attrs={'name': 'description'}):
            summary = art_soup.find('meta', attrs={'name': 'description'}).get('content', '')
        # FAQ
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
            'author': author,
            'summary': summary,
            'faq': faq
        }
    except Exception as e:
        logging.warning(f"Falha ao coletar artigo {url_art}: {e}")
        return None

if __name__ == "__main__":
    extract_articles_from_html()
