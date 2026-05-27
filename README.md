# Papelaria Forward

## Descrição do projeto 📄

O projeto apresenta um gerenciamento de vendas e a listagem de comissões. Nele, é possível cadastrar uma venda com seus produtos e associá-la a um vendedor e a um cliente. Além disso, cada venda pode ser atualizada ou excluída.

Também é possível consultar a lista de comissões por vendedor, com base nas vendas realizadas e nos percentuais de comissão definidos para os produtos.

## Stack

- Python 3.12+
- Django 6
- Django REST Framework
- django-cors-headers
- PostgreSQL (desenvolvimento)

## Estrutura do Projeto

```text
.
├── Makefile
├── docker-compose.yml
├── README.md
└── backend/
	├── pyproject.toml
	├── uv.lock
	├── manage.py
	├── pytest.ini
	├── apps/
	│   └── core/
	├── config/
	├── .env.example
	└── db.sqlite3
```

## Pré-requisitos

- Python 3.12 ou superior
- uv instalado
- Docker e Docker Compose (Opcional)

Instalação do uv (Linux/macOS):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Quick Start (Makefile)

Execute os comandos na raiz do projeto:

```bash
cp backend/.env.example backend/.env
uv venv .venv --python 3.12
source .venv/bin/activate
make install
make migrate
make dev
```

Aplicação disponível em: `http://127.0.0.1:8000/`

## Automação com Makefile

O projeto possui um `Makefile` na raiz para facilitar tarefas do dia a dia.

Listar todos os comandos disponíveis:

```bash
make help
```

Comandos mais usados:

- Instalar dependências: `make install`
- Subir servidor local: `make dev`
- Rodar testes: `make test`
- Rodar lint (`ruff` + `mypy`): `make lint`
- Formatar código (`ruff format`): `make format`
- Limpar caches e arquivos temporários: `make clean`
- Aplicar migrações: `make migrate`
- Criar migração (informando app): `make migrate-create app=nome_do_app`
- Resetar banco e carregar fixtures: `make setup`
- Executar checagens de segurança (`bandit` e `pip-audit`): `make security`

Comandos Docker:

- Subir containers: `make docker-up`
- Derrubar containers: `make docker-down`

## Fluxo Alternativo (sem Makefile)

1. Crie o ambiente virtual na raiz do projeto:

```bash
uv venv .venv --python 3.12
```

2. Ative o ambiente virtual:

```bash
source .venv/bin/activate
```

3. Configure as variáveis de ambiente:

```bash
cp backend/.env.example backend/.env
```

4. Sincronize as dependências definidas em `backend/pyproject.toml` e `backend/uv.lock`:

```bash
cd backend
uv sync
```

5. Aplique as migrações:

```bash
python manage.py migrate
```

6. Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

- Com Docker:
```bash
docker compose up --build
```

## Rotas Disponíveis

- Admin Django: `http://127.0.0.1:8000/admin/`

## Popular banco com fixtures

O projeto possui um comando de setup que limpa o banco e carrega os dados iniciais de fixtures.

Ambiente local:

```bash
make setup
```

Com Docker:

```bash
docker compose exec api python manage.py setup --yes
```

> Atenção: esse comando executa `flush` e apaga todos os dados atuais antes de popular novamente.

O projeto usa `backend/config/settings.py` para os ambientes normais e `backend/config/settings_test.py` para testes.


## Gerenciamento de Dependências com uv

Adicionar uma dependência ao projeto:

```bash
cd backend
uv add nome-do-pacote
```

Adicionar dependência de desenvolvimento:

```bash
cd backend
uv add --dev nome-do-pacote
```

Remover uma dependência:

```bash
cd backend
uv remove nome-do-pacote
```

Sincronizar ambiente após alterações no lockfile:

```bash
cd backend
uv sync
```

## Variáveis de Ambiente

Exemplo em `backend/.env.example`:

- `SECRET_KEY`: chave secreta do Django.
- `DEBUG`: `True` para desenvolvimento local.
- `ALLOWED_HOSTS`: hosts permitidos separados por vírgula.
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `DB_HOST` e `DB_PORT`: configuram o PostgreSQL do ambiente local e do Docker.
- `backend/config/settings_test.py` isola a configuração de testes.

## Observações

- O CORS está aberto para todas as origens (`CORS_ALLOW_ALL_ORIGINS = True`) na configuração atual.
- A paginação padrão da API está definida com 20 itens por página no DRF.
