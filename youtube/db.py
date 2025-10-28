import psycopg2
from datetime import datetime

class Database:
    def __init__(self, settings):
        self.settings = settings
        self.conn = psycopg2.connect(
            host=settings.DB_HOST,
            database=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            port=getattr(settings, 'DB_PORT', 5432)
        )
    
    def _parse_date(self, date_str):
        if not date_str or date_str == "Data não disponível":
            return None
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except:
            try:
                return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z')
            except:
                return None

    def video_exists(self, video_id):
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM transcricoes WHERE video_id = %s", (video_id,))
            return cursor.fetchone()[0] > 0

    def save_video(self, video):
        with self.conn as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO transcricoes (video_id, titulo, descricao, data_publicacao, canal, transcricao, 
                                             view_count, like_count, comment_count, duracao, url, thumbnail, tags)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (video_id) DO NOTHING;
                    """,
                    (
                        video.video_id,
                        video.title,
                        video.description,
                        self._parse_date(video.published_at),
                        video.channel_id,
                        video.transcricao or "",
                        video.view_count,
                        video.like_count,
                        video.comment_count,
                        video.duration,
                        video.url,
                        video.thumbnail,
                        video.tags
                    )
                )
