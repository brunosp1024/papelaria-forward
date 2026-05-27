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
├── pyproject.toml
├── README.md
└── backend/
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

## Configuração do Ambiente com uv

1. Crie o ambiente virtual na raiz do projeto:

```bash
uv venv .venv --python 3.12
```

2. Ative o ambiente virtual:

```bash
source .venv/bin/activate
```

3. Sincronize as dependências definidas em `pyproject.toml` e `uv.lock`:

```bash
uv sync
```

4. Configure as variáveis de ambiente:

```bash
cp backend/.env.example backend/.env
```

5. Entre na pasta do backend e aplique as migrações:

```bash
cd backend
python manage.py migrate
```

6. Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

- com Docker:
```bash
docker compose up --build
```

Aplicação disponível em: `http://127.0.0.1:8000/`

## Rotas Disponíveis

- Admin Django: `http://127.0.0.1:8000/admin/`

## Popular banco com fixtures

O projeto possui um comando de setup que limpa o banco e carrega os dados iniciais de fixtures.

Ambiente local:

```bash
cd backend
python manage.py setup --yes
```

Com Docker:

```bash
docker compose exec api python manage.py setup --yes
```

> Atenção: esse comando executa `flush` e apaga todos os dados atuais antes de popular novamente.

## Comandos Úteis

Executar testes Django:

```bash
cd backend
pytest
```

O projeto usa `backend/config/settings.py` para os ambientes normais e `backend/config/settings_test.py` para testes.


## Gerenciamento de Dependências com uv

Adicionar uma dependência ao projeto:

```bash
uv add nome-do-pacote
```

Adicionar dependência de desenvolvimento:

```bash
uv add --dev nome-do-pacote
```

Remover uma dependência:

```bash
uv remove nome-do-pacote
```

Sincronizar ambiente após alterações no lockfile:

```bash
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
