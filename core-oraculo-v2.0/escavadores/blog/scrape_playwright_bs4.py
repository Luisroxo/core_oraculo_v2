import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import random
import json

# Configurações de evasão
USER_AGENTS = [
    # Exemplos de user-agents modernos
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

BLOG_URL = "https://www.kommo.com/br/blog/"

async def get_html_with_playwright(url):
    user_agent = random.choice(USER_AGENTS)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Modo visual
        context = await browser.new_context(user_agent=user_agent, viewport={"width": 1920, "height": 1080})
        page = await context.new_page()
        # Maximiza a janela do navegador
        await page.set_viewport_size({"width": 1920, "height": 1080})
        await page.evaluate("window.moveTo(0,0);")
        await page.evaluate("window.resizeTo(screen.width,screen.height);")

        # Aguarda o carregamento da página
        await page.goto(url)
        await page.wait_for_load_state('load', timeout=60000)

        # Tenta detectar e fechar o modal logo após o carregamento
        try:
            await page.wait_for_selector('button.ub-emb-close', timeout=5000)
            print("Modal detectado. Fechando automaticamente...")
            try:
                await page.click('button.ub-emb-close', force=True)
                print("Modal fechado com force=True.")
            except Exception:
                await page.evaluate('document.querySelector("button.ub-emb-close").click()')
                print("Modal fechado via JavaScript.")
        except Exception as e:
            print(f"Modal não detectado ou erro ao fechar: {e}")

        # Imprime parte do HTML inicial para diagnóstico
        html_init = await page.content()
        print("\n--- INÍCIO HTML DA PÁGINA PRINCIPAL ---")
        print(html_init[:10000])
        print("--- FIM HTML DA PÁGINA PRINCIPAL ---\n")

        # Não busca mais por seletor de artigo, apenas retorna o HTML da página
        print("--- INÍCIO HTML FINAL ---")
        html_final = await page.content()
        print(html_final[:10000])
        print("--- FIM HTML FINAL ---")
        await browser.close()
        return html_final

async def extract_article_links():
    html = await get_html_with_playwright(BLOG_URL)
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    # Busca todos os <a> que contenham '/br/blog/' no href e não sejam páginas de índice
    for a in soup.find_all('a', href=True):
        href = a['href']
        if '/br/blog/' in href and not href.rstrip('/').endswith(('noticias', 'blog', 'vendas-conversacionais')):
            full_url = href if href.startswith('http') else f'https://www.kommo.com{href}'
            links.add(full_url)
    return list(links)

async def extract_article_details(url):
    html = await get_html_with_playwright(url)
    soup = BeautifulSoup(html, "html.parser")
    # Valida se é página de artigo (tem título e conteúdo principal)
    title = ""
    h1 = soup.select_one('div[id^="page"] h1')
    if h1:
        title = h1.get_text(strip=True)
    else:
        h1 = soup.find("h1")
        if h1:
            title = h1.get_text(strip=True)
    # Conteúdo principal: busca múltiplos blocos
    content_blocks = []
    for sel in [
        'div[id^="page"] div.blog-article__content',
        'div[id^="page"] div[class*="content"]',
        'div[id^="page"] div[class*="article"]',
        'div[id^="page"] div[class*="text"]',
        'div[id^="page"] div[class*="body"]',
    ]:
        for div in soup.select(sel):
            content_blocks.append(div.get_text("\n", strip=True))
    # Se não achou, tenta blocos genéricos
    if not content_blocks:
        content_div = soup.find("div", class_="blog-article__content")
        if content_div:
            content_blocks.append(content_div.get_text("\n", strip=True))
    content = "\n".join(content_blocks)
    # Data de publicação
    pub_date = ""
    time_tag = soup.find("time")
    if time_tag:
        pub_date = time_tag.get_text(strip=True)
    # Autor
    author = ""
    author_tag = soup.select_one('div[id^="page"] h6')
    if author_tag:
        author = author_tag.get_text(strip=True)
    # Resumo
    summary = ""
    summary_div = soup.find("div", class_="blog-article__toc")
    if summary_div:
        summary = summary_div.get_text("\n", strip=True)
    # Só retorna se for artigo válido
    if title and content:
        return {
            "title": title,
            "url": url,
            "content": content,
            "published_at": pub_date,
            "author": author,
            "summary": summary
        }
    else:
        print(f"Página ignorada (não é artigo): {url}")
        return None

async def main():
    print("Coletando links de artigos...")
    links = await extract_article_links()
    print(f"Total de links encontrados: {len(links)}")
    for i, link in enumerate(links, 1):
        print(f"{i:02d}: {link}")
    print("\nExtraindo detalhes dos artigos...")
    artigos = []
    for link in links:
        artigo = await extract_article_details(link)
        if artigo:
            artigos.append(artigo)
            print(f"\n--- {artigo['title']} ---\nURL: {artigo['url']}\nAutor: {artigo['author']}\nData: {artigo['published_at']}\nResumo: {artigo['summary']}\nConteúdo: {artigo['content'][:300]}...")

    print(f"\nTotal de artigos extraídos: {len(artigos)}")
    # Exporta para JSON
    with open("artigos_extraidos.json", "w", encoding="utf-8") as f:
        json.dump(artigos, f, ensure_ascii=False, indent=2)
    print("\nArtigos exportados para artigos_extraidos.json")

if __name__ == "__main__":
    asyncio.run(main())
