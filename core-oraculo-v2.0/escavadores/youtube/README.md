
# Escavador YouTube

Microsserviço responsável por coletar dados de múltiplos canais do YouTube, com suporte nativo a múltiplos canais.

## Execução local
```bash
docker build -t escavador-youtube .
docker run --rm --network=host escavador-youtube
```

## Configuração de múltiplos canais
No arquivo `.env`, defina a variável `CHANNEL_IDS` como uma lista separada por vírgula:

```
CHANNEL_IDS=UC123,UC456,UC789
```

Se `CHANNEL_IDS` não estiver definida, o sistema usará `CHANNEL_ID` ou `ESCAVADOS_CHANNEL_ID` para retrocompatibilidade.

## Integração com Mensageria
- Consome mensagens da fila `escavador_youtube`.
- Publica resultados conforme padrão de mensagens do orquestrador.
