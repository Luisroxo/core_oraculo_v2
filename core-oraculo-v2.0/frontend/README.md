# Dashboard de Monitoramento do Pipeline

Este frontend tem como objetivo monitorar, auditar e gerenciar o pipeline de transcrição do YouTube.

## Recomendações Técnicas
- Visualização em tempo real do progresso dos lotes, status das transcrições e uso de recursos (CPU/RAM).
- Alertas automáticos para falhas, lentidão ou problemas de rate limit.
- Histórico de erros, tentativas e vídeos processados.
- Integração fácil com notificações (e-mail, Slack).
- Facilidade para ajustar parâmetros e acompanhar impacto das mudanças.
- Relatórios para auditoria e tomada de decisão.

## Stack Sugerida
- Backend API: FastAPI ou Flask
- Frontend: Streamlit, Dash, ou React/Vue
- Coleta de métricas: psutil (CPU/RAM), logs do Python, status do banco
- Gráficos: Plotly, Chart.js ou nativo do framework
- Autenticação: JWT ou OAuth2

## Estrutura Inicial
- `app.py`: Inicialização do dashboard (exemplo Streamlit)
- `metrics.py`: Coleta de métricas do pipeline
- `alerts.py`: Lógica de alertas e notificações
- `config_dashboard.py`: Parâmetros configuráveis do dashboard
- `static/` e `templates/`: Para frontend customizado (caso use Flask)
