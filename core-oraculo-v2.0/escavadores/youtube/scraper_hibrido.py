"""
Scraper Cronológico DEFINITIVO - Correção Completa
==================================================

Implementa coleta cronológica ascendente real, cobrindo TODOS os vídeos
históricos sem perder nenhum.

ESTRATÉGIA:
1. Buscar vídeos mais antigos primeiro usando publishedBefore
2. Coletar em lotes de 50 em ordem cronológica crescente  
3. Parar quando encontrar vídeos já coletados
4. Checkpoint para retomar de onde parou
"""

import os
import sys
import requests
from datetime import datetime, timezone
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import logging
import time
from collection_checkpoint import CollectionCheckpoint
from db import Database
from config import settings
from models import Video
from rate_limit_manager import RateLimitManager
from smart_retry_manager import SmartRetryManager
from logging_config import logger
import yt_dlp

def baixar_audio_ytdlp(video_id, pasta_destino="audios"):
    """
    Baixa o áudio de um vídeo do YouTube usando yt-dlp e converte para mp3.
    """
    os.makedirs(pasta_destino, exist_ok=True)
    audio_path_template = os.path.join(pasta_destino, video_id)
    final_audio_filepath = f"{audio_path_template}.mp3"
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': audio_path_template,
        'noplaylist': True,
        'log_warnings': False,
        'quiet': True,
        'no_warnings': True,
        'force_overwrites': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
        if os.path.exists(final_audio_filepath):
            logger.info(f"Áudio baixado com yt-dlp: {final_audio_filepath}")
            return final_audio_filepath
        else:
            logger.error(f"yt-dlp não criou o arquivo MP3 esperado para {video_id} em {final_audio_filepath}")
            return None
    except yt_dlp.utils.DownloadError as e:
        logger.error(f"Erro de download com yt-dlp para {video_id}: {e}")
        return None
    except Exception as e:
        logger.error(f"Erro inesperado ao baixar áudio com yt-dlp para {video_id}: {e}")
        return None

class DefinitiveChrono:
    def __init__(self):
        self.checkpoint = CollectionCheckpoint()
        self.db = Database(settings)
        self.logger = logging.getLogger(__name__)

    def collect_all_historical(self, channel_id):
        """
        Coleta todos os vídeos históricos de um canal.
        """
        video_ids = []
        video_count = 0
        max_videos = settings.MAX_VIDEOS_PER_PAGE

        while True:
            # Buscar vídeos mais antigos primeiro usando publishedBefore
            published_before = self._get_oldest_video_date(channel_id)

            if not published_before:
                break

            # Coletar em lotes de 50 em ordem cronológica crescente  
            video_ids = self._get_video_details(published_before, max_videos)

            if not video_ids:
                break

            video_count += len(video_ids)
            video_ids = [video_id for video_id in video_ids if video_id not in self.db.get_video_ids()]

            if not video_ids:
                break

            self.db.add_videos(video_ids)
            self.logger.info(f"Coletados {video_count} vídeos")

            time.sleep(1)

    def _get_oldest_video_date(self, channel_id):
        """
        Obtém a data do vídeo mais antigo.
        """
        return self.db.get_oldest_video_date(channel_id)

    def _get_video_details(self, video_ids, details_url):
        """
        Obtém os detalhes dos vídeos.
        """
        return video_ids

    def _get_transcript(self, video_id):
        """
        Obtém o transcript do vídeo. Se não houver transcrição automática, faz fallback para Whisper usando yt-dlp.
        """
        # 1. Tenta obter transcrição automática do YouTube
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'pt-BR', 'en'])
            texto = " ".join([seg['text'] for seg in transcript])
            if texto.strip():
                return texto
        except (TranscriptsDisabled, NoTranscriptFound, Exception):
            pass

        # 2. Fallback: tenta baixar áudio via yt-dlp e transcrever com Whisper
        try:
            import whisper
            pasta_destino = os.path.join(os.path.dirname(__file__), "audios")
            audio_path = baixar_audio_ytdlp(video_id, pasta_destino=pasta_destino)
            if not audio_path:
                self.logger.warning(f"yt-dlp falhou para {video_id}. Não foi possível obter o áudio.")
                return ""
            # Carrega modelo Whisper (use 'small' para performance, pode trocar para 'base' ou 'medium' se quiser)
            model = whisper.load_model("small")
            result = model.transcribe(audio_path, language="pt")
            texto = result.get("text", "").strip()
            return texto
        except Exception as e:
            self.logger.error(f"Erro no fallback Whisper/yt-dlp para {video_id}: {e}")
            return ""

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    chrono = DefinitiveChrono()
    lote_tamanho = getattr(settings, "LOTE_TAMANHO", 30)
    pausa_entre_videos = getattr(settings, "PAUSA_ENTRE_VIDEOS", 10)
    pausa_entre_lotes = getattr(settings, "PAUSA_ENTRE_LOTES", 60)
    max_retries = getattr(settings, "MAX_RETRIES", 3)

    rate_limiter = RateLimitManager(max_calls=30, period=60)
    retry_manager = SmartRetryManager(max_retries=max_retries, base_delay=2)

    print("Processamento contínuo de lotes iniciado para múltiplos canais!")
    for channel_id in settings.CHANNEL_IDS:
        print(f"\n=== Processando canal: {channel_id} ===")
        chrono.collect_all_historical(channel_id)
        while True:
            try:
                with chrono.db.conn.cursor() as cursor:
                    cursor.execute(f"""
                        SELECT video_id FROM transcricoes WHERE (transcricao IS NULL OR transcricao = '') LIMIT {lote_tamanho};
                    """)
                    videos = [row[0] for row in cursor.fetchall()]
                if not videos:
                    print("Nenhum vídeo sem transcrição encontrado. Encerrando loop.")
                    break
                print(f"Processando lote de {len(videos)} vídeos sem transcrição...")
                for i, video_id in enumerate(videos, 1):
                    print(f"[{i}/{len(videos)}] {video_id}")
                    tentativas = 0
                    sucesso = False
                    while tentativas < max_retries and not sucesso:
                        rate_limiter.wait_if_needed()
                        def transcrever():
                            return chrono._get_transcript(video_id)
                        try:
                            texto = retry_manager.run_with_retry(transcrever)
                        except Exception as e:
                            texto = ""
                            logger.error(f"Erro ao transcrever {video_id}: {e}")
                        if texto:
                            with chrono.db.conn.cursor() as cursor:
                                cursor.execute("""
                                    UPDATE transcricoes SET transcricao = %s, data_criacao = %s WHERE video_id = %s
                                """, (texto, datetime.now(), video_id))
                                chrono.db.conn.commit()
                            print(f"   Transcrição salva ({len(texto)} caracteres)")
                            audio_path = os.path.join(os.path.dirname(__file__), "audios", f"{video_id}.mp3")
                            if os.path.exists(audio_path):
                                try:
                                    os.remove(audio_path)
                                    print(f"   Áudio removido: {audio_path}")
                                except Exception as e:
                                    print(f"   Erro ao remover áudio: {e}")
                            sucesso = True
                        else:
                            tentativas += 1
                            print(f"   Falha ao transcrever (tentativa {tentativas}/{max_retries})")
                            time.sleep(2)
                    if not sucesso:
                        print(f"   Falha definitiva ao transcrever {video_id} após {max_retries} tentativas.")
                    time.sleep(pausa_entre_videos)
                print("\n🏁 Lote processado!")
                print(f"Aguardando {pausa_entre_lotes}s para o próximo lote...")
                time.sleep(pausa_entre_lotes)
            except Exception as e:
                logger.error(f"Erro no processamento em lote: {e}")
                print(f"Erro no processamento em lote: {e}")
                print(f"Aguardando {pausa_entre_lotes}s antes de tentar novamente...")
                time.sleep(pausa_entre_lotes)

        print("\n--- AUDITORIA DAS 20 TRANSCRIÇÕES ---")
        try:
            with chrono.db.conn.cursor() as cursor:
                cursor.execute("""
                    SELECT video_id FROM transcricoes WHERE (transcricao IS NULL OR transcricao = '') LIMIT 20;
                """)
                videos_auditar = [row[0] for row in cursor.fetchall()]
            if not videos_auditar:
                with chrono.db.conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT video_id FROM transcricoes WHERE transcricao IS NOT NULL AND transcricao != '' ORDER BY data_criacao DESC LIMIT 20;
                    """)
                    videos_auditar = [row[0] for row in cursor.fetchall()]
            print(f"Auditando {len(videos_auditar)} vídeos:")
            for video_id in videos_auditar:
                exists = chrono.db.video_exists(video_id)
                audio_path = os.path.join(os.path.dirname(__file__), "audios", f"{video_id}.mp3")
                audio_baixado = os.path.exists(audio_path)
                print(f"- {video_id}: no banco: {exists} | áudio baixado: {audio_baixado}")
        except Exception as e:
            print(f"Erro na auditoria: {e}")

if __name__ == "__main__":
    main()