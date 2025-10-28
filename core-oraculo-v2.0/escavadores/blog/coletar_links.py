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
import psycopg2
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()
DB_URL = os.getenv('DB_URL')
DB_PASSWORD = os.getenv('DB_PASSWORD')

BLOG_URL = "https://www.kommo.com/br/blog/"

def get_conn():
    return psycopg2.connect(DB_URL)

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

async def extract_links_from_category(url_categoria):
    print(f'Coletando artigos da categoria: {url_categoria}')
    pagina = 1
    paginas_visitadas = set()
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    url_pagina = url_categoria
    total_novos = 0
    while url_pagina and url_pagina not in paginas_visitadas:
        print(f'Coletando página {pagina}: {url_pagina}')
        paginas_visitadas.add(url_pagina)
        html = await get_html_with_playwright(url_pagina)
        soup = BeautifulSoup(html, "html.parser")
        novos_links = set()
        for a in soup.select('a.article-card'):
            href = a.get('href')
            if href and href.startswith('/br/blog/'):
                full_url = f'https://www.kommo.com{href}'
                novos_links.add(full_url)
        destaque_topo = soup.select_one('.article-card__preview--big a[href]')
        if destaque_topo:
            href = destaque_topo.get('href')
            if href and href.startswith('/br/blog/'):
                full_url = f'https://www.kommo.com{href}'
                novos_links.add(full_url)
        destaque_rodape = soup.select_one('.article-card-big a[href]')
        if destaque_rodape:
            href = destaque_rodape.get('href')
            if href and href.startswith('/br/blog/'):
                full_url = f'https://www.kommo.com{href}'
                novos_links.add(full_url)
        novos_inseridos = 0
        for link in novos_links:
            try:
                cur.execute('INSERT INTO links_coletados (url, tipo) VALUES (%s, %s) ON CONFLICT (url) DO NOTHING;', (link, 'conteudo'))
                novos_inseridos += cur.rowcount
            except Exception as e:
                print(f'Erro ao inserir {link}: {e}')
        conn.commit()
        print(f'Página {pagina}: {len(novos_links)} links encontrados, {novos_inseridos} inseridos.')
        total_novos += novos_inseridos
        # Busca o link da próxima página na paginação (apenas o maior número)
        next_page = None
        paginacao = soup.select('ul.flex li a[href*="/page/"]')
        max_num = pagina
        for a in paginacao:
            href = a.get('href')
            if href and href.startswith('/br/blog/'):
                import re
                match = re.search(r'/page/(\d+)', href)
                if match:
                    num = int(match.group(1))
                    if num > max_num:
                        max_num = num
                        next_page = f'https://www.kommo.com{href}'
        if next_page and next_page not in paginas_visitadas:
            url_pagina = next_page
            pagina = max_num
        else:
            break
    cur.close()
    conn.close()
    print(f'Total de novos links de artigos inseridos da categoria: {total_novos}')

async def extract_links_from_all_categories():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("SELECT url FROM links_coletados WHERE tipo = 'categoria'")
    categorias = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    print(f'Encontradas {len(categorias)} categorias para varrer.')
    for url_categoria in categorias:
        await extract_links_from_category(url_categoria)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "todas":
        async def fluxo_completo():
            # Garante que a tabela existe antes de qualquer operação
            conn = get_conn()
            cur = conn.cursor()
            cur.execute(CREATE_TABLE_SQL)
            conn.commit()
            cur.close()
            conn.close()
            # Coleta links de categorias e insere no banco
            print('Coletando links de categorias da página principal...')
            # Lista completa de categorias
            categorias = [
                'comunidade', 'ia', 'instagram', 'linkedin', 'listas', 'news', 'novidades',
                'perfil-comercial-no-google', 'shopify', 'tiktok', 'todos', 'vendas', 'vendas-conversacionais',
                'whatsapp', 'alternativas', 'empreendedorismo', 'fundamentos-crm', 'integracoes', 'marketing',
                'noticias', 'parceiros', 'robo-de-vendas', 'crm', 'botao-de-chat-web'
            ]
            # Gera URLs de todas as categorias
            links_categorias = [(f'https://www.kommo.com/br/blog/{cat}/', 'categoria') for cat in categorias]
            conn = get_conn()
            cur = conn.cursor()
            for link, tipo in links_categorias:
                try:
                    cur.execute('INSERT INTO links_coletados (url, tipo) VALUES (%s, %s) ON CONFLICT (url) DO NOTHING;', (link, tipo))
                except Exception as e:
                    print(f'Erro ao inserir categoria {link}: {e}')
            conn.commit()
            cur.close()
            conn.close()
            # Agora varre todas as categorias
            await extract_links_from_all_categories()
        asyncio.run(fluxo_completo())
    elif len(sys.argv) > 1 and sys.argv[1].startswith("http"):
        asyncio.run(extract_links_from_category(sys.argv[1]))
    else:
        print("Uso: python coletar_links.py todas | <url_categoria>")

async def extract_links_from_all_categories():
    conn = psycopg2.connect(os.getenv('DB_URL'))
    cur = conn.cursor()
    cur.execute("SELECT url FROM links_coletados WHERE tipo = 'categoria'")
    categorias = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    print(f'Encontradas {len(categorias)} categorias para varrer.')
    for url_categoria in categorias:
        await extract_links_from_category(url_categoria)
import psycopg2
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

# NOVA FUNÇÃO: Coleta links de artigos em todas as categorias do banco
async def extract_links_from_categories():
    # Conecta ao banco para buscar links de categoria
    conn = psycopg2.connect(os.getenv('DB_URL'))
    cur = conn.cursor()
    cur.execute("SELECT url FROM links_coletados WHERE tipo = 'categoria'")
    categorias = [row[0] for row in cur.fetchall()]
    print(f'Encontradas {len(categorias)} categorias para varrer.')
    total_novos = 0
    for url_categoria in categorias:
        print(f'Coletando artigos da categoria: {url_categoria}')
        page_num = 1
        while True:
            url_pagina = url_categoria
            if page_num > 1:
                url_pagina = url_categoria.rstrip('/') + f'/?page={page_num}'
            html = await get_html_with_playwright(url_pagina)
            soup = BeautifulSoup(html, "html.parser")
            novos_links = set()
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('/br/blog/') and not href.rstrip('/').split('/')[-1] in ['blog', 'noticias']:
                    slug = href.rstrip('/').split('/')[-1]
                    if slug not in [c.split('/')[-1] for c in categorias]:
                        full_url = f'https://www.kommo.com{href}'
                        novos_links.add(full_url)
            # Salva novos links no banco
            novos_inseridos = 0
            for link in novos_links:
                try:
                    cur.execute('INSERT INTO links_coletados (url, tipo) VALUES (%s, %s) ON CONFLICT (url) DO NOTHING;', (link, 'conteudo'))
                    novos_inseridos += cur.rowcount
                except Exception as e:
                    print(f'Erro ao inserir {link}: {e}')
            conn.commit()
            print(f'Página {page_num}: {len(novos_links)} links encontrados, {novos_inseridos} inseridos.')
            total_novos += novos_inseridos
            # Verifica se há paginação (se não encontrar novos links, para)
            if not novos_links:
                break
            page_num += 1
    cur.close()
    conn.close()
    print(f'Total de novos links de artigos inseridos a partir das categorias: {total_novos}')

async def main():
    # Conecta e cria tabela
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(CREATE_TABLE_SQL)
    conn.commit()
    print('Tabela links_coletados pronta.')

    # Coleta links da página principal
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

    # Coleta links de artigos em todas as categorias
    await extract_links_from_categories()
    cur.close()
    conn.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "todas":
        asyncio.run(extract_links_from_all_categories())
    elif len(sys.argv) > 1 and sys.argv[1].startswith("http"):
        asyncio.run(extract_links_from_category(sys.argv[1]))
    else:
        print("Uso: python coletar_links.py todas | <url_categoria>")
