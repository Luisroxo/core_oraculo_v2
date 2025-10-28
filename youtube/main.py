"""
Integração do escavador YouTube principal com o submódulo youtube_scraper.
Executa o scraping e persistência no banco usando as credenciais do .env.
"""
import os
import psycopg2
from dotenv import load_dotenv

# Carrega variáveis do .env local
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

def test_db_connection():
    db_url = os.getenv('DB_URL')
    if not db_url:
        print('DB_URL não encontrada no .env')
        return
    try:
        conn = psycopg2.connect(db_url)
        print('Conexão com o banco de dados estabelecida com sucesso!')
        conn.close()
    except Exception as e:
        print(f'Erro ao conectar ao banco de dados: {e}')

if __name__ == "__main__":
    test_db_connection()