
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

class Settings:
    """
    Configuração centralizada do escavador YouTube.

    Suporte nativo a múltiplos canais:
        - Defina CHANNEL_IDS no .env como uma lista separada por vírgula.
            Exemplo: CHANNEL_IDS=UC123,UC456,UC789
        - Se CHANNEL_IDS não estiver definida, utiliza CHANNEL_ID ou ESCAVADOS_CHANNEL_ID para retrocompatibilidade.

    Parâmetros disponíveis:
        - DB_URL, DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT: conexão com banco de dados
        - YOUTUBE_API_KEY: chave da API do YouTube
        - CHANNEL_IDS: lista de IDs de canais a serem processados
        - LOTE_TAMANHO, PAUSA_ENTRE_VIDEOS, PAUSA_ENTRE_LOTES, MAX_RETRIES: controle de processamento em lote

    Para testes, use Settings(load_env=False) para evitar carregamento do .env.
    """
    def __init__(self, load_env=True):
        if load_env:
            load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
        self.DB_URL = os.getenv("DB_URL")
        if self.DB_URL:
            parsed = urlparse(self.DB_URL)
            self.DB_HOST = parsed.hostname or "localhost"
            self.DB_NAME = parsed.path.lstrip('/')
            self.DB_USER = parsed.username or "postgres"
            self.DB_PASSWORD = parsed.password or ""
            self.DB_PORT = parsed.port or 5432
        else:
            self.DB_HOST = os.getenv("DB_HOST", "localhost")
            self.DB_NAME = os.getenv("DB_NAME", "oraculo")
            self.DB_USER = os.getenv("DB_USER", "postgres")
            self.DB_PASSWORD = os.getenv("DB_PASSWORD", "")
            self.DB_PORT = int(os.getenv("DB_PORT", 5432))
        self.YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
        # Suporte nativo a múltiplos canais
        self.CHANNEL_IDS = [id.strip() for id in (os.getenv("CHANNEL_IDS") or "").split(',') if id.strip()]
        # Para retrocompatibilidade, inclui CHANNEL_ID único se definido
        if not self.CHANNEL_IDS:
            channel_id_single = os.getenv("CHANNEL_ID") or os.getenv("ESCAVADOS_CHANNEL_ID")
            if channel_id_single:
                self.CHANNEL_IDS = [channel_id_single.strip()]

        # Parâmetros do processamento em lote
        self.LOTE_TAMANHO = int(os.getenv("LOTE_TAMANHO", 30))
        self.PAUSA_ENTRE_VIDEOS = int(os.getenv("PAUSA_ENTRE_VIDEOS", 10))
        self.PAUSA_ENTRE_LOTES = int(os.getenv("PAUSA_ENTRE_LOTES", 60))
        self.MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))

settings = Settings()
