# PeçaBot API

Este projeto utiliza FastAPI e Docker Compose para fornecer uma solução de API web escalável e fácil de implantar.

## Pré-requisitos

Antes de começar, certifique-se de ter o [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/) instalados em sua máquina.

## Instalação e Execução

1. Clone o repositório:

    ```bash
    git clone https://github.com/caiomagri/chabot_api.git
    cd chatbot_api
    ```

2. Crie um arquivo `.env` com as configurações necessárias. Veja o exemplo em [Configuração](#configuração).

3. Inicie os serviços usando Docker Compose:

    ```bash
    docker-compose up -d
    ```

4. Acesse a API em [http://localhost:8000](http://localhost:8000).

5. Para parar os contêineres, execute:

    ```bash
    docker-compose down
    ```

## Configuração

Atualize o arquivo `.env` com as configurações necessárias:

```bash
# Configurações do Chatbot e do Sistema de Comércio Eletrônico

# Escolha o tipo de chatbot (chatterbot ou openai)
CHATBOT_TYPE=

# Nome do chatbot (opcional)
CHATBOT_NAME=
CHATBOT_STORAGE_ADAPTER=
CHATBOT_DATABASE_URI=

# Configurações da OpenAI (se usar)
OPENAI_TOKEN=
OPENAI_CHAT_MODEL=
OPENAI_MAX_TOKENS=
OPENAI_TOP_P=
OPENAI_FREQUENCY_PENALTY=
OPENAI_PRESENCE_PENALTY=

# Configurações do Sistema de Comércio Eletrônico (ECOM)
BASE_ECOMMERCE_URL=
ECOMMERCE_SECRET_KEY=
DATABASE_ECOMMERCE_URI=

# Escolha o mecanismo de busca do comércio eletrônico (llm ou api)
ECOMMERCE_SEARCH_ENGINE=
```