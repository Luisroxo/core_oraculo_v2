# Coleta de métricas do pipeline
import psutil

def get_pipeline_metrics():
    # Exemplo: coletar métricas do sistema e pipeline
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    # Simulação de dados do pipeline
    videos_processados = 1200
    videos_pendentes = 45
    historico_lotes = [20, 22, 18, 30, 25, 28, 30]
    return {
        "cpu": cpu,
        "ram": ram,
        "videos_processados": videos_processados,
        "videos_pendentes": videos_pendentes,
        "historico_lotes": historico_lotes,
    }
