# Magic Deckbuilder API

## Rotas

### Decks

| Método | Rota | Descrição |
|--------|-------|------------|
| `GET /deck` | Lista todos os decks | |
| `GET /deck/:id` | Obtém um deck pelo ID | |
| `GET /deck/name/:name` | Obtém um deck pelo nome | |
| `POST /deck` | Cria um deck manualmente (ex: nome, formato, descrição etc.) | |
| `PUT /deck/:id` | Atualiza informações do deck (nome, formato etc.) | |
| `DELETE /deck/:id` | Exclui o deck | |
| `GET /deck/:id/stats` | Retorna estatísticas (curva de mana, cores, tipos de carta, etc) | |

### Importação / Exportação

| Método | Rota | Descrição |
|--------|-------|------------|
| `GET /deck/:id/txt` | Baixa o deck como `.txt` | |
| `GET /deck/:id/csv` | Baixa o deck como `.csv` | |
| `POST /deck/import/txt` | Cria um deck a partir de um arquivo `.txt` | |
| `POST /deck/import/csv` | Cria um deck a partir de um arquivo `.csv` | |

### Cartas dentro de um Deck

| Método | Rota | Descrição |
|--------|-------|------------|
| `POST /deck/:id/card` | Adiciona uma carta ao deck | |
| `PUT /deck/:id/card/:cardId` | Atualiza a quantidade de uma carta no deck | |
| `DELETE /deck/:id/card/:cardId` | Remove uma carta do deck | |

### Cartas

| Método | Rota | Descrição |
|--------|-------|------------|
| `GET /card` | Lista todas as cartas salvas localmente | |
| `GET /card/:id` | Busca carta pelo ID local | |
| `GET /card/name/:name` | Busca carta pelo nome (local) | |
| `GET /card/commander/` | Busca todos os commanders | |
| `GET /card/search/:query` | Busca na API Scryfall | |
| `GET /card/autocomplete/:query` | Autocompleta nomes de carta (Scryfall) | |
| `POST /card` | Salva uma carta manualmente (opcional, se quiser armazenar) | |
| `POST /card/random` | Busca carta aleatória | |

## Estrutura Visual das Rotas

```
/
├── deck
│   ├── (GET) - Lista todos os decks
│   ├── (POST) - Cria um deck
│   ├── :id
│   │   ├── (GET) - Obtém um deck
│   │   ├── (PUT) - Atualiza o deck
│   │   ├── (DELETE) - Exclui o deck
│   │   ├── stats (GET) - Retorna estatísticas
│   │   ├── txt (GET) - Baixa como .txt
│   │   ├── csv (GET) - Baixa como .csv
│   │   └── card
│   │       ├── (POST) - Adiciona uma carta
│   │       └── {cardId}
│   │           ├── (PUT) - Atualiza a quantidade
│   │           └── (DELETE) - Remove uma carta
│   ├── name
│   │   └── :name (GET) - Obtém um deck pelo nome
│   └── import
│       ├── txt (POST) - Cria deck de .txt
│       └── csv (POST) - Cria deck de .csv
└── card
    ├── (GET) - Lista todas as cartas locais
    ├── (POST) - Salva uma carta manualmente
    ├── :id (GET) - Busca carta pelo ID local
    ├── name
    │   └── :name (GET) - Busca carta pelo nome local
    ├── commander (GET) - Busca todos os commanders
    ├── search
    │   └── :query (GET) - Busca na API Scryfall
    ├── autocomplete
    │   └── :query (GET) - Autocompleta nomes (Scryfall)
    └── random (POST) - Busca carta aleatória
```

## Tecnologias Utilizadas

O backend deste projeto foi desenvolvido com foco em simplicidade, desempenho e facilidade de manutenção.  
A stack principal inclui:

| Tecnologia | Função |
|-------------|--------|
| **Python** | Linguagem principal utilizada no backend. Escolhida pela clareza e pelo forte ecossistema de bibliotecas. |
| **FastAPI** | Framework web assíncrono para criação de APIs REST de alta performance e tipadas. |
| **SQLite** | Banco de dados relacional leve e embutido, ideal para projetos locais. |

Outras tecnologias utilizadas:

| Categoria | Tecnologia | Justificativa |
|------------|-------------|----------------|
| **ORM / Camada de Dados** | [SQLAlchemy](https://www.sqlalchemy.org/) | Simplifica a manipulação do banco de dados com modelos tipados e migrações. |
| **Validação e Tipagem** | [Pydantic](https://docs.pydantic.dev/) | Usado pelo FastAPI para validação de dados e tipagem automática. |
| **Testes** | [Pytest](https://pytest.org/) | Framework de testes simples e poderoso para garantir a qualidade do código. |
| **Documentação da API** | [OpenAPI / Swagger](https://swagger.io/specification/) | Geração automática de documentação interativa da API. |
| **Logs e Monitoramento** | [Loguru](https://github.com/Delgan/loguru), [Sentry](https://sentry.io/) | Registro e rastreamento de erros. |

## Requisitos para Execução

Antes de executar o projeto, verifique se o ambiente atende aos seguintes requisitos mínimos:

| Tipo | Requisito | Descrição |
|------|------------|-----------|
| **Sistema Operacional** | Windows / Linux / macOS | Compatível com qualquer sistema que suporte Python 3.10+ |
| **Versão do Python** | ≥ 3.10 | FastAPI e SQLAlchemy recomendam versões mais recentes do Python |
| **Banco de Dados** | SQLite (padrão) | Cria um arquivo local `.db`, sem necessidade de servidor externo |
| **Gerenciador de Pacotes** | pip ou uv | Usado para instalar as dependências do projeto |

### Dependências Principais

```bash
pip install fastapi uvicorn sqlalchemy pydantic
```

### Dependências de Desenvolvimento (opcionais)

```bash
pip install pytest loguru
```

## Executando o Servidor

Após instalar as dependências, inicie o servidor FastAPI com o comando:

```bash
uvicorn app.main:app --reload
```

Por padrão, o servidor será iniciado em:

```
http://127.0.0.1:8000
```

A documentação interativa da API estará disponível em:

```
http://127.0.0.1:8000/docs
```

## Como Utilizar

1. Crie seus decks usando os endpoints da rota `/deck`.
2. Importe decks em formato `.txt` ou `.csv` pela rota `/deck/import`.
3. Busque cartas usando `/card/search` ou adicione manualmente com `/card`.
4. Visualize estatísticas e exporte seus decks em `.txt` ou `.csv`.
5. Consulte a documentação interativa para testar endpoints diretamente pelo navegador.

### Estrutura Recomendada de Pastas

```
project/
├── app/
│   ├── main.py              # Ponto de entrada do FastAPI
│   ├── models/              # Modelos e schemas (SQLAlchemy / Pydantic)
│   ├── routes/              # Rotas organizadas por módulo (deck, card)
│   ├── services/            # Regras de negócio e integrações externas (Scryfall)
│   ├── database.py          # Configuração do banco SQLite
│   └── utils/               # Funções auxiliares
├── tests/                   # Testes automatizados (pytest)
├── requirements.txt         # Dependências do projeto
└── README.md
```

