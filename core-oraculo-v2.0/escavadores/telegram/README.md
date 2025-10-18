# Escavador Telegram

Microsserviço responsável por coletar dados do Telegram.

## Execução local
```bash
docker build -t escavador-telegram .
docker run --rm --network=host escavador-telegram
```

## Integração com Mensageria
- Consome mensagens da fila `escavador_telegram`.
- Publica resultados conforme padrão de mensagens do orquestrador.
