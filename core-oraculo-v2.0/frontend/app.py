# Exemplo inicial de dashboard com Streamlit
import streamlit as st
from metrics import get_pipeline_metrics
from alerts import check_alerts

st.set_page_config(page_title="Dashboard Pipeline YouTube", layout="wide")
st.title("Monitoramento do Pipeline de Transcrição YouTube")

# Métricas principais
data = get_pipeline_metrics()
st.metric("Vídeos processados", data["videos_processados"])
st.metric("Vídeos pendentes", data["videos_pendentes"])
st.metric("CPU (%)", data["cpu"])
st.metric("RAM (%)", data["ram"])

# Alertas
tipo_alerta, mensagem = check_alerts(data)
if tipo_alerta:
    st.warning(f"Alerta: {mensagem}")

# Gráficos e histórico
st.subheader("Histórico de Processamento")
st.line_chart(data["historico_lotes"])

# ...expandir para configurações, logs, notificações...
