# Escavador Licitações

Microsserviço responsável por coletar dados de licitações.

## Execução local
```bash
docker build -t escavador-licitacoes .
docker run --rm --network=host escavador-licitacoes
```

## Integração com Mensageria
- Consome mensagens da fila `escavador_licitacoes`.
- Publica resultados conforme padrão de mensagens do orquestrador.
