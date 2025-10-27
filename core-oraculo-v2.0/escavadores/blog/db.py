import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'), override=True)

DB_URL = os.getenv("DB_URL")

def get_connection():
    return psycopg2.connect(DB_URL, cursor_factory=RealDictCursor)

def save_articles(articles, fonte):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS blog_articles (
            id SERIAL PRIMARY KEY,
            fonte VARCHAR(20),
            categoria VARCHAR(50),
            title TEXT,
            url TEXT UNIQUE,
            content TEXT,
            published_at TIMESTAMP,
            reading_time VARCHAR(20),
            views INTEGER,
            author TEXT,
            summary TEXT,
            faq JSONB,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    for art in articles:
        # Validação: não insere se não houver url ou title
        if not art.get('url') or not art.get('title'):
            continue
        published_at = art.get('published_at')
        if not published_at or (isinstance(published_at, str) and published_at.strip() == ''):
            published_at = None
        try:
            cur.execute(
                """
                INSERT INTO blog_articles (
                    fonte, categoria, title, url, content, published_at, reading_time, views, author, summary, faq
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (url) DO UPDATE SET
                    categoria = EXCLUDED.categoria,
                    content = EXCLUDED.content,
                    published_at = EXCLUDED.published_at,
                    reading_time = EXCLUDED.reading_time,
                    views = EXCLUDED.views,
                    author = EXCLUDED.author,
                    summary = EXCLUDED.summary,
                    faq = EXCLUDED.faq
                """,
                (
                    fonte,
                    art.get('categoria'),
                    art.get('title'),
                    art.get('url'),
                    art.get('content'),
                    published_at,
                    art.get('reading_time'),
                    art.get('views'),
                    art.get('author'),
                    art.get('summary'),
                    psycopg2.extras.Json(art.get('faq')) if art.get('faq') else None
                )
            )
        except Exception as e:
            print(f"Erro ao inserir artigo {art.get('url')}: {e}")
    conn.commit()
    cur.close()
    conn.close()
