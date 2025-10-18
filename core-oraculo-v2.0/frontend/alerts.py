# Lógica de alertas e notificações

def check_alerts(data):
    if data["cpu"] > 90:
        return "CPU", "Uso de CPU acima de 90%"
    if data["ram"] > 90:
        return "RAM", "Uso de RAM acima de 90%"
    if data["videos_pendentes"] > 100:
        return "Pipeline", "Muitos vídeos pendentes!"
    return None, None
