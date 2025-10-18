# 🦩 Arquitetura de Escavadores e Executadores por Fonte de Dados (Modelo ORÁCULO)

## ⚡ Visão Geral

Para o projeto **ORÁCULO**, a forma como os microsserviços são estruturados tem impacto direto na **velocidade de pesquisa**, **criação de conteúdo** e **comunicação interna** do sistema.

O modelo adotado e oficial será a **Arquitetura de Escavadores e Executadores por Fonte de Dados**, que define uma separação clara entre:
- **Escavadores (INPUT):** responsáveis pela coleta de dados.  
- **Executadores (OUTPUT):** responsáveis pela criação de conteúdo e entrega de resultados processados.  

---

## 🧱 Arquitetura de Escavadores por Fonte de Dados

Nesta arquitetura, cada microsserviço **Escavador** é especializado em coletar dados de **uma única fonte específica**, garantindo desempenho, isolamento e fácil manutenção.

### 🔹 Exemplos de Escavadores

- **Escavador YouTube** – Responsável pela coleta de vídeos, comentários e metadados.  
- **Escavador Blog** – Focado na extração de conteúdo de blogs e portais.  
- **Escavador Telegram** – Coleta mensagens e mídias de canais e grupos.  
- **Escavador Instagram** – Captura posts, stories e engajamentos.  
- **Escavador Facebook** – Coleta posts, comentários e estatísticas.  
- **Escavador WhatsApp** – Registra mensagens e interações públicas.  
- **Escavador Licitações** – Extrai editais e documentos de portais públicos (ComprasNet, BLL Compras, etc.).  

---

## 🦩 Arquitetura de Executadores (Camada de Criação)

Os **Executadores** são microsserviços voltados à **produção automatizada de conteúdo e resultados**, com base nos dados coletados pelos Escavadores e organizados pelo Core ORÁCULO.

### 🔹 Exemplos de Executadores

- **Executador de Relatórios** – Gera relatórios PDF, CSV ou Markdown.  
- **Executador de Conteúdo (IA)** – Produz textos, resumos, descrições e artigos com IA generativa.  
- **Executador de Mídias Sociais** – Cria e publica postagens automaticamente nas plataformas integradas.  
- **Executador de Automações** – Dispara processos em CRMs, ERPs, e fluxos de e-mail.  
- **Executador ERP/CRM** – Atualiza registros e dispara ações com base em insights coletados.  

---

## ⚙️ Características Principais

- **Especialização por Função:**  
  Escavadores lidam com **coleta de dados**, enquanto Executadores lidam com **criação e publicação**.  

- **Independência Total:**  
  Cada serviço é autônomo e comunica-se via **mensageria (RabbitMQ/Redis)**, garantindo isolamento e escalabilidade.  

- **Escalabilidade Fina:**  
  Tanto Escavadores quanto Executadores podem ser escalados horizontalmente conforme a demanda de uma fonte ou tipo de entrega.  

- **Ciclo Fechado de Informação:**  
  Dados são **coletados → processados → convertidos em entregas automáticas** (posts, relatórios, insights, automações).  

---

## 🚀 Velocidade de Pesquisa e Criação

Nesta arquitetura, o desempenho é otimizado em duas camadas:

### 🔸 Coleta (Escavadores)
- **Otimização de desempenho por fonte.**  
- **Paralelização total** entre escavadores.  
- **Escalabilidade independente.**  
- **Resiliência a falhas de origem.**

### 🔸 Criação (Executadores)
- **Processamento paralelo de tarefas criativas.**  
- **Integração com APIs de IA e automação.**  
- **Publicação e entrega automática de resultados.**  
- **Reprocessamento de falhas sem afetar o restante do pipeline.**

---

## 🔄 Velocidade de Comunicação

A comunicação entre os microsserviços é **assíncrona e desacoplada**, mediada pelo **Core ORÁCULO** e pela **mensageria**.

### Principais Benefícios
- **Comunicação focada e leve.**  
- **Desacoplamento entre coleta e criação.**  
- **Filas dedicadas por tipo de tarefa (input/output).**  
- **Alta resiliência e recuperação automática.**

---

## 🧑‍💻 Conclusão: Modelo ORÁCULO

O **Modelo ORÁCULO** integra duas camadas complementares:

| Camada | Responsabilidade | Resultado |
|--------|------------------|-----------|
| **Escavadores** | Coletar dados de múltiplas fontes (APIs, Web, Portais) | Dados estruturados e normalizados |
| **Executadores** | Criar e publicar resultados com base nos dados coletados | Conteúdo, relatórios, insights, automações |
| **Core ORÁCULO** | Orquestrar o fluxo entre coleta e criação | Coordenação, agregação e entrega final |

Este modelo entrega:
- Alta **velocidade** na coleta e produção.  
- **Desacoplamento** total entre camadas.  
- **Escalabilidade horizontal** por serviço.  
- **Automação inteligente** do ciclo de informação.  

---

## 🦩 Stack Tecnológico por Microserviço

| Componente | Stack Tecnológico | Função Principal |
|-------------|------------------|------------------|
| **Core ORÁCULO** | - **Python (FastAPI)**<br>- **RabbitMQ / Celery**<br>- **Redis** (cache e estado)<br>- **PostgreSQL** (metadados)<br>- **Docker / Kubernetes** | Orquestra escavadores e executadores, gerencia filas e consolida dados |
| **Escavador YouTube** | - **Python (yt-dlp / YouTube Data API)**<br>- **BeautifulSoup4 / Playwright**<br>- **Pandas** | Coleta vídeos, comentários e metadados |
| **Escavador Blog** | - **Requests + BeautifulSoup4**<br>- **Feedparser / LangChain / LlamaIndex** | Captura posts e artigos de blogs e portais |
| **Escavador Telegram** | - **Telethon (Python)**<br>- **AsyncIO / WebSocket** | Coleta mensagens, mídias e metadados |
| **Escavador Instagram** | - **Instaloader / Playwright**<br>- **GraphQL API** | Coleta posts, stories e interações |
| **Escavador Facebook** | - **Facebook Graph API / Playwright** | Coleta posts, comentários e métricas |
| **Escavador WhatsApp** | - **Node.js (Baileys / WWebJS)** | Coleta conversas e mensagens públicas integradas |
| **Escavador Licitações** | - **Playwright / Selenium**<br>- **PDFMiner / PyMuPDF / SpaCy** | Coleta e analisa editais e licitações públicas |
| **Executador de Relatórios** | - **Python (ReportLab / Pandas / Jinja2)** | Geração automática de relatórios (PDF, CSV, MD) |
| **Executador de Conteúdo (IA)** | - **Python + OpenAI / Ollama API**<br>- **LangChain / Transformers** | Geração de textos, posts e resumos automatizados |
| **Executador de Mídias Sociais** | - **Node.js / Puppeteer / Meta API / Twitter API** | Publicação e agendamento de conteúdos em redes sociais |
| **Executador de Automações / ERP / CRM** | - **Python (Requests / Zapier / Kommo API / Bling API)** | Disparo de automações e integração com sistemas externos |
| **Data Lake / Repositório** | - **MongoDB / MinIO / S3 / PostgreSQL**<br>- **Airbyte / Apache Nifi** | Armazenamento bruto, versionamento e integração de dados |
| **Monitoramento / Logs** | - **Prometheus + Grafana + ELK Stack** | Observabilidade e rastreabilidade de microsserviços |
| **CI/CD e Deploy** | - **GitHub Actions / Docker / K8s / Helm** | Automação de build, testes e deploy contínuo |

---

## 🦩 Observações Técnicas

- Todos os serviços seguem o padrão **microservice + message broker**.  
- Cada serviço é **stateless**, permitindo **auto-escalonamento horizontal**.  
- Comunicação padronizada via **JSON + RabbitMQ**.  
- Logs centralizados no formato **ELK (Elastic Stack)**.  
- Segurança e autenticação baseadas em **JWT + API Gateway (Kong ou Nginx)**.  
- Suporte nativo a **eventos temáticos e filas dinâmicas** para escavadores e executadores.  

