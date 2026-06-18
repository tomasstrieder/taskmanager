# Trabalho Grau B
# Engenharia de Software
# Luíza Birck e Tomás Strieder

# taskmanager
API REST para colaboração em tarefas com cadastro e autenticação de usuários.

---

## Documentação

- **ReDoc**: [http://localhost:8000/redoc] — documentação gerada por Swagger/OpenAPI

---

## Instruções para instalação (Docker, recomendado)

**Pré-requisitos**: Docker Desktop, Git

```bash
# 1. Clonar repositório
git clone <url>
cd taskmanager

# 2. Criar .env
copy .env.example .env
# Opcionalmente abrir .env e definir uma SECRET_KEY

# 3. Rodar
docker compose up --build -d
```

# 4. Swagger UI
A API estará disponpível em `http://localhost:8000/docs`.

# 5. Testando endpoints
- Para testar os endpoints:
    - Realize o login (`/auth/login`) 
    - Copie o `access_token`
    - Clique em **Authorize** (no topo da página)
    - Cole o token

# 8. Extras
- Para consultar os logs (ou utilizar a interface do Docker)
```bash
docker compose logs app -f
```
- Para parar a execução
```bash
docker compose down
```

---

## Instruções para instalação (localmente)

**Pré-requisitos**: Python 3.12+, Git, PostgreSQL

```bash
# 1. Clonar o repositório
git clone <url>
cd taskmanager

# 2. Criar o ambiente virtual
python -m venv .venv
.venv\Scripts\activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Criar .env
cp .env.example .env
# Opcionalmente abrir .env e definir uma SECRET_KEY

# 5. Abrir PostgreSQL e executar o seguinte para criar os bancos de dados:
  CREATE DATABASE taskmanager;
  CREATE DATABASE taskmanager_test;

# 6. Realizar migrações
alembic upgrade head

# 7. Rodar o servidor
uvicorn app.main:app --reload
```

# 8. Swagger UI
A API estará disponpível em `http://localhost:8000/docs`.
A partir daí o funcionamento é o mesmo.

---

## Testes
Para rodar os testes automatizados:

# Se rodando o projeto em Docker:
```bash
docker compose exec app pytest

# Ou, com relatório de cobertura
docker compose run --rm app pytest --cov=app --cov-report=term-missing
```

# Ou, se rodando localmente:

```bash
pytest

# Ou, com relatório de cobertura
pytest --cov=app --cov-report=term-missing
```

---

## Extra: seed.py e clean.py
Os seguintes scripts ,localizados na root do projeto, foram desenvolvidos para popular/depopular o banco de dados mais facilmente:
- seed.py: Cria 3 usuários, 9 tarefas e 27 comentários (3 para cada) .
- clean.py: Limpa o banco de todos os usuários, tarefas e comentários.
Para rodar, simplesmente:

# Em Docker:
```bash
docker compose exec app python seed.py

docker compose exec app python clean.py
```

# Localmente:
```bash
# Ativar o ambiente caso não ativo
.venv\Scripts\activate

python seed.py

python clean.py
```

---

## Logging

- Logs são enviados para a saída padrão (stdout) no nível INFO.

- Quando usando Docker, utilize `docker compose logs app -f` para acompanhar os logs.

- Quando rodando localmente, logs são escritos em `app.log`.

---

## Stacks utilizadas

- Framework: FastAPI
- Banco de dados: PostgreSQL 16
- ORM: SQLAlchemy 2.0
- Migrações: Alembic
- Validação: Pydantic v2
- Autenticação: JWT e bcrypt
- Testes: pytest
- Container: Docker e Docker Compose

---

## Arquitetura

O projeto segue o padrão Clean Architecture com separação entre camadas:

app/
├── api/
│   ├── dependencies/     # Auth dependency injection
│   └── routes/           # HTTP route handlers
├── services/             # Business logic
├── repositories/         # Database queries
├── models/               # SQLAlchemy ORM models
├── schemas/              # Pydantic request/response schemas
├── core/                 # Config, security, logging, exceptions
├── database/             # Session and base setup
└── tests/                # pytest test suite

---

## Modelo de dados

### User
| Campo           | Tipo     |
|-----------------|----------|
| id              | int      |
| name            | str      |
| email           | str      |
| hashed_password | str      |
| role            | enum     |
| is_active       | bool     |
| created_at      | datetime |

### Task
| Campo       | Tipo      |
|-------------|-----------|
| id          | int       |
| title       | str       |
| description | str       |
| status      | enum      |
| priority    | enum      |
| due_date    | date      |
| created_by  | FK → User |
| assigned_to | FK → User |
| created_at  | datetime  |
| updated_at  | datetime  |

### Comment
| Campo      | Tipo      |
|------------|-----------|
| id         | int       |
| content    | str       |
| task_id    | FK → Task |
| user_id    | FK → User |
| created_at | datetime  |

---

## API Endpoints

### Auth
| Método | Path           | Descrição   |
|--------|----------------|-------------|
| POST   | `/auth/login`  | Logar       |
| POST   | `/auth/logout` | Deslogar    |

### Users
| Método | Path               | Descrição                |
|--------|--------------------|--------------------------|
| POST   | `/users`           | Cadastrar novo usuário   |
| GET    | `/users/{user_id}` | Consultar usuário por ID |
| PUT    | `/users/{user_id}` | Atualizar usuário        |
| DELETE | `/users/{user_id}` | Deletar usuário          |

### Tasks
| Método | Path               | Descrição                          |
|--------|--------------------|------------------------------------|
| POST   | `/tasks`           | Cadastrar nova tarefa              |
| GET    | `/tasks`           | Listar tarefas (filtros avançados) |
| GET    | `/tasks/{task_id}` | Consultar tarefas por ID           |
| PUT    | `/tasks/{task_id}` | Atualizar tarefa                   |
| DELETE | `/tasks/{task_id}` | Deletar tarefa                     |

**Filtros** : `status`, `priority`, `assignedTo`, `dueBefore`, `dueAfter`

### Comments
| Método | Path                        | Descrição                 |
|--------|-----------------------------|---------------------------|
| POST   | `/tasks/{task_id}/comments` | Cadastrar novo comentário |
| GET    | `/tasks/{task_id}/comments` | Consultar comentários     |
| DELETE | `/comments/{comment_id}`    | Deletar comentário        |

### Metrics
| Método | Path       | Descrição           |
|--------|------------|---------------------|
| GET    | `/metrics` |  Consultar métricas |

---