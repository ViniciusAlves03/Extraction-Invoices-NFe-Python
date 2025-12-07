# Serviço de Extração (Extraction Service)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google%20bard&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)

Este é o repositório do Serviço de Extração. Ele é responsável por receber arquivos de notas fiscais, em formato de imagem ou planilha, processá-los e transformar dados não estruturados em informações organizadas. O serviço utiliza Google Gemini AI para interpretar imagens de notas fiscais (OCR inteligente) e Pandas para processar arquivos Excel.

Ele é responsável por gerenciar as **despesas (expenses)** dos usuários. Ele permite que usuários registrem e consultem suas transações de despesa, associando-as a um usuário (`userId`) e, opcionalmente, a uma categoria (`categoryId`).

Construído com Python e FastAPI, este projeto segue princípios de **Clean Architecture** e **Domain-Driven Design (DDD)** para garantir um código desacoplado, testável e de fácil manutenção.

## ✨ Principais Funcionalidades

* **Processamento de Arquivos:**
    * Suporte a upload de planilhas (`.xlsx`, `.xls`) e imagens (`.png`, `.jpg`, `.jpeg`).
* **Inteligência Artificial (OCR)**
    * Integração com `Google Gemini` para ler, interpretar e extrair dados de notas fiscais (NFe/DANFE) a partir de imagens.
* **Extração de Excel:**
    * Processamento de planilhas para leitura em lote de despesas utilizando `pandas`.
* **Histórico de Tarefas:**
    * Mantém um registro de todas as tarefas de extração (`ExtractionTask`), permitindo acompanhar o status (`PENDING`, `COMPLETED`, `PARTIAL_SUCCESS`, `FAILED`) e visualizar relatórios de erros.
* **Validação de Dados:**
    * Validação robusta de IDs (Mongo ObjectIds), datas (formato YYYY-MM-DD) e campos obrigatórios.
* **Arquitetura Robusta:**
    * Uso de `dependency-injector` para gestão de contêineres e `Beanie` como ODM assíncrono para MongoDB.

## 🚀 Tecnologias Utilizadas

* **Linguagem:** Python 3.11+
* **Framework API:** FastAPI
* **Injeção de Dependência:** dependency-injector
* **Banco de Dados:** MongoDB
* **ODM:** Beanie
* **AI & LLM:** Google Gemini API (Generative AI)
* **Manipulação de Dados:** Pandas
* **Validação:** Pydantic
* **Documentação:** Swagger / OpenAPI

## 📋 Pré-requisitos

Para executar este projeto localmente, você precisará ter os seguintes serviços instalados e em execução:

* Python +3.11.0
* MongoDB
* [API Key](https://ai.google.dev/gemini-api/docs/api-key?hl=pt-br) do Google Gemini válida.

## ⚙️ Instalação e Execução

Existem duas formas de rodar o projeto em desenvolvimento.

### Método 1: Rodando com Docker (Recomendado)

Este método é o mais simples, pois usa o Dockerfile para executar a aplicação, e Docker Compose para subir a aplicação e o banco de dados (MongoDB) localmente.

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/ViniciusAlves03/Extraction-Invoices-NFe-Python
    cd Extraction-Invoices-NFe-Python
    ```

2.  **Configure as variáveis de ambiente:**
    Crie um arquivo `.env` na raiz do projeto, baseado no `.env.example`. Você pode usar o seguinte comando:
    ```bash
    cp .env.example .env
    ```

3.  **Inicie a aplicação e o MongoDB:**
    Use o arquivo `docker-compose.yml` para iniciar os containers das dependências em background.
    ```bash
    docker-compose up -d --build
    ```
    * MongoDB estará disponível em: `localhost:27017`
    * A aplicação estará sendo executada em `http://localhost:3000`.

---
### Método 2: Rodando Localmente (Sem Docker)

Este método exige que você tenha o **MongoDB** rodando na sua máquina local.

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/ViniciusAlves03/Extraction-Invoices-NFe-Python.git
    cd Extraction-Invoices-NFe-Python
    ```

2.  **Crie o ambiente virtual e instale as dependências:**
    ```bash
    python -m venv venv
    venv/scripts/activate
    pip install -r requirements.txt
    ```

3.  **Configure as variáveis de ambiente:**
    Crie um arquivo `.env` na raiz do projeto, baseado no `.env.example`. Você pode usar:
    ```bash
    cp .env.example .env
    ```

4.  **Inicie a aplicação:**
    ```bash
    uvicorn src.app:create_app --factory --host 0.0.0.0 --port 3000 --reload
    ```

## 🏗️ Estrutura do Projeto

```sh
src/
├── application/           # Regras de negócio
│   ├── domain/            # Núcleo do domínio (Modelos, Exceções, Validadores)
│   ├── port/              # Interfaces (Ports) para repositórios e serviços
│   └── service/           # Casos de uso (ExtractionService)
│
├── infrastructure/        # Implementação técnica
│   ├── adapter/           # Adaptadores externos (GeminiExtractor, ExcelExtractor)
│   ├── database/          # Conexão Mongo e Schemas do Beanie
│   ├── entity/            # Mappers (Domain <-> Schema)
│   └── repository/        # Implementação dos repositórios
│
├── ui/                    # Interface de entrada
│   ├── controller/        # Rotas do FastAPI
│   └── exception/         # Tratamento global de erros e respostas JSON
│
├── di/                    # Contêiner de Injeção de Dependência
├── utils/                 # Utilitários (Logger, Settings, Hashing)
└── app.py                 # Fábrica da aplicação FastAPI
```

## 📖 Visão Geral da API (Endpoints)

A API foca no recurso de Extrações vinculado a usuários.

Para uma documentação interativa completa, com detalhes de *schemas* e *body*, acesse a documentação do Swagger:
**`http://localhost:3000/docs`**

### 📄 Extractions

Rotas para informar e consultar as extrações.

| Método | Rota (Path) | Descrição |
| :--- | :--- | :--- |
| `POST` | `/v1/users/{user_id}/extractions/` | Envia um arquivo (Excel ou Imagem) para processamento e extração de dados. Retorna a tarefa criada. |
| `GET` | `/v1/users/{user_id}/extractions/` | Lista o histórico de tarefas de extração do usuário. Suporta filtros por `status`, `title`, `date`, `categoryId` e `isDuplicate`. |
| `GET` | `/v1/users/{user_id}/extractions/{task_id}` | Obtém os detalhes completos de uma tarefa de extração específica, incluindo os itens extraídos e relatórios de erro. |

---

## 🧑‍💻 Autor <a id="autor"></a>

<p align="center">Desenvolvido por Vinícius Alves <strong><a href="https://github.com/ViniciusAlves03">(eu)</a></strong>.</p>

---
