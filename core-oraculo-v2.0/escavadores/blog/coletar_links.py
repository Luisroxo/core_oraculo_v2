import psycopg2
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import re 

# --- Configurações ---
load_dotenv()
DB_URL = os.getenv('DB_URL')
BLOG_URL = "https://www.kommo.com/br/blog/"
TIPO_PADRAO = 'pendente' # Novo tipo padrão para links não classificados

# --- Funções de Banco de Dados ---

def get_conn( ):
    """Retorna uma nova conexão com o banco de dados PostgreSQL."""
    if not DB_URL:
        raise ValueError("DB_URL não definida! Verifique o arquivo .env.")
    return psycopg2.connect(DB_URL)

CREATE_TABLE_SQL = '''
CREATE TABLE IF NOT EXISTS links_coletados (
    id SERIAL PRIMARY KEY,
    url TEXT UNIQUE NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    coletado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
'''

# --- Funções de Web Scraping ---

async def get_html_with_playwright(page, url):
    """Obtém o HTML de uma URL usando uma instância de página Playwright já aberta."""
    await page.goto(url)
    # Mantendo a espera por seletor e o fechamento de modal para garantir o carregamento completo
    try:
        await page.wait_for_selector('.blog-article__content, .article-card', timeout=15000)
    except Exception:
        pass # Ignora seletor principal se não encontrado
        
    # Tenta detectar e fechar o modal (mantido do seu código)
    try:
        await page.wait_for_selector('button.ub-emb-close', timeout=5000)
        await page.click('button.ub-emb-close', force=True)
    except Exception:
        pass 
        
    html = await page.content()
    return html

async def extract_all_blog_links(page):
    """Coleta todos os links internos do blog a partir da página principal."""
    print(f'Coletando links da página: {BLOG_URL}')
    html = await get_html_with_playwright(page, BLOG_URL)
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    
    for a in soup.find_all('a', href=True):
        href = a['href']
        # Filtra apenas links que começam com /br/blog/
        if href.startswith('/br/blog/'):
            full_url = f'https://www.kommo.com{href}'
            links.add(full_url )
            
    return list(links)

# --- Fluxo de Execução (FASE 1 - Coleta Bruta) ---

async def fase_1_coleta_bruta():
    """Executa a Fase 1: Coleta bruta e salvamento no BD com tipo 'pendente'."""
    
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(CREATE_TABLE_SQL)
    conn.commit()
    
    print('Iniciando Fase 1: Coleta Bruta de links da página principal...')
    
    # Inicializa o Playwright e o Browser APENAS UMA VEZ
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # 1. Coleta de URLs
        links_coletados = await extract_all_blog_links(page)
        
        inseridos = 0
        
        # 2. Inserção no Banco de Dados com TIPO_PADRAO
        print(f'\n--- Inserindo {len(links_coletados)} links no BD com tipo="{TIPO_PADRAO}" ---')
        for link in links_coletados:
            
            try:
                # Insere URL e TIPO_PADRAO
                cur.execute('INSERT INTO links_coletados (url, tipo) VALUES (%s, %s) ON CONFLICT (url) DO NOTHING;', (link, TIPO_PADRAO))
                inseridos += cur.rowcount
            except Exception as e:
                print(f'Erro ao inserir {link}: {e}')
                
        conn.commit()
        await browser.close()
        
        print(f'\nFase 1 Concluída. Total de links inseridos/atualizados: {inseridos}')
        
    cur.close()
    conn.close()

# --- Ponto de Entrada ---

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "todas":
        asyncio.run(fase_1_coleta_bruta())
        print("\n--- Comandos para versionar no git ---")
        print("git add core-oraculo-v2.0/escavadores/blog/coletar_links.py")
        print("git commit -m 'feat: coleta bruta de links do blog sem classificação'")
        print("git push")
    else:
        print("Uso: python coletar_links.py todas")
