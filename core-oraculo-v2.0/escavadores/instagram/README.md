# Escavador Instagram

Microsserviço responsável por coletar dados do Instagram.

## Execução local
```bash
docker build -t escavador-instagram .
docker run --rm --network=host escavador-instagram
```

## Integração com Mensageria
- Consome mensagens da fila `escavador_instagram`.
- Publica resultados conforme padrão de mensagens do orquestrador.
