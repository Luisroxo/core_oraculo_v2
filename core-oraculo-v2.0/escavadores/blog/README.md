# Escavador Blog

Microsserviço responsável por coletar dados de blogs.

## Execução local
```bash
docker build -t escavador-blog .
docker run --rm --network=host escavador-blog
```

## Integração com Mensageria
- Consome mensagens da fila `escavador_blog`.
- Publica resultados conforme padrão de mensagens do orquestrador.
