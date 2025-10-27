import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import psycopg2
import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()
DB_URL = os.getenv('DB_URL')
DB_PASSWORD = os.getenv('DB_PASSWORD')

BLOG_URL = "https://www.kommo.com/br/blog/"

# Função para conectar ao banco
def get_conn():
    return psycopg2.connect(DB_URL)

# Cria tabela se não existir
CREATE_TABLE_SQL = '''
CREATE TABLE IF NOT EXISTS links_coletados (
    id SERIAL PRIMARY KEY,
    url TEXT UNIQUE NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    coletado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
'''

async def get_html_with_playwright(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_load_state('load', timeout=60000)
        html = await page.content()
        await browser.close()
        return html

async def extract_article_links():
    html = await get_html_with_playwright(BLOG_URL)
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    categorias = [
        'comunidade', 'ia', 'instagram', 'linkedin', 'listas', 'news', 'novidades',
        'perfil-comercial-no-google', 'shopify', 'tiktok', 'todos', 'vendas', 'vendas-conversacionais',
        'whatsapp', 'alternativas', 'empreendedorismo', 'fundamentos-crm', 'integracoes', 'marketing',
        'noticias', 'parceiros', 'robo-de-vendas', 'crm', 'botao-de-chat-web'
    ]
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('/br/blog/'):
            slug = href.rstrip('/').split('/')[-1]
            if slug in categorias:
                tipo = 'categoria'
            else:
                tipo = 'conteudo'
            full_url = f'https://www.kommo.com{href}'
            links.add((full_url, tipo))
    return list(links)

async def main():
    # Conecta e cria tabela
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(CREATE_TABLE_SQL)
    conn.commit()
    print('Tabela links_coletados pronta.')

    # Coleta links
    print('Coletando links de artigos e categorias...')
    links = await extract_article_links()
    print(f'Total de links encontrados: {len(links)}')

    # Insere links no banco, ignorando duplicados
    for link, tipo in links:
        try:
            cur.execute('INSERT INTO links_coletados (url, tipo) VALUES (%s, %s) ON CONFLICT (url) DO NOTHING;', (link, tipo))
        except Exception as e:
            print(f'Erro ao inserir {link}: {e}')
    conn.commit()
    print('Links salvos no banco.')
    cur.close()
    conn.close()

if __name__ == "__main__":
    asyncio.run(main())
