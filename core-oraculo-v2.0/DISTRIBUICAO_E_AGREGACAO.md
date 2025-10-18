# Distribuição de Tarefas e Agregação de Resultados

## Visão Geral
Esta etapa do Orquestrador Core é responsável por:
- Distribuir tarefas para múltiplos escavadores e executadores de forma paralela (fan-out).
- Agregar e correlacionar os resultados recebidos (fan-in), garantindo consistência, tolerância a falhas e escalabilidade.

## Fluxo de Distribuição de Tarefas
1. **Recebimento da solicitação**: O orquestrador recebe um pedido de coleta/execução via API ou mensagem.
2. **Identificação dos destinos**: Com base no tipo de tarefa, determina quais escavadores/executadores devem ser acionados.
3. **Geração de mensagens**: Para cada destino, gera uma mensagem com `correlation_id`, `tipo_evento`, `payload` e `timestamp`.
4. **Envio para a fila**: Publica as mensagens nas filas apropriadas (RabbitMQ, Redis Streams, etc).
5. **Monitoramento de status**: Mantém controle dos status de cada subtarefa (pendente, em execução, concluída, erro, timeout).

## Estratégias de Agregação de Resultados
- **Fan-in**: O orquestrador aguarda o retorno de todos os escavadores/executadores ou até um timeout configurável.
- **Correlações**: Utiliza o `correlation_id` para associar respostas às requisições originais.
- **Timeouts e tolerância a falhas**: Resultados não recebidos até o timeout são marcados como erro/timeout, mas não bloqueiam o fluxo.
- **Agregação**: Os resultados são consolidados em um único payload, que pode ser retornado via API ou publicado em outra fila.

## Exemplo de Fluxo (Pseudocódigo)
```python
# Recebe solicitação de orquestração
correlation_id = gerar_correlation_id()
tarefas = ["escavador_youtube", "escavador_blog", "executador_relatorio"]
for destino in tarefas:
    mensagem = {
        "correlation_id": correlation_id,
        "tipo_evento": "iniciar_coleta",
        "payload": {...},
        "timestamp": now()
    }
    enviar_para_fila(destino, mensagem)

# Aguarda respostas (fan-in)
resultados = aguardar_respostas(correlation_id, len(tarefas), timeout=30)
# Agrega e retorna
return agregar_resultados(resultados)
```

## Requisitos Técnicos
- Uso de filas/mensageria (RabbitMQ, Redis Streams, etc).
- Mensagens com `correlation_id` único para cada orquestração.
- Estrutura de dados para controle de status das subtarefas.
- Timeout configurável para agregação.
- Logs detalhados para rastreabilidade.

## Referências
- [Padrão Fan-out/Fan-in](https://docs.microsoft.com/pt-br/azure/architecture/patterns/fan-out-fan-in)
- [Celery Canvas: Group, Chord](https://docs.celeryq.dev/en/stable/userguide/canvas.html)

---

> **Próximos passos:**
> - Implementar estrutura de código para distribuição e agregação.
> - Integrar com mensageria e persistência de status.
> - Testes de tolerância a falhas e escalabilidade.
