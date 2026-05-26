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
	├── config/
	├── core/
	├── .env.example
	└── db.sqlite3
```

## Pré-requisitos

- Python 3.12 ou superior
- uv instalado

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

Aplicação disponível em: `http://127.0.0.1:8000/`

## Rotas Disponíveis

- Admin Django: `http://127.0.0.1:8000/admin/`

## Comandos Úteis

Executar testes Django:

```bash
cd backend
python manage.py test
```

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
- `DATABASE_URL`: presente no exemplo, mas atualmente a configuração ativa usa SQLite via `BASE_DIR / "db.sqlite3"`.

## Observações

- O CORS está aberto para todas as origens (`CORS_ALLOW_ALL_ORIGINS = True`) na configuração atual.
- A paginação padrão da API está definida com 20 itens por página no DRF.
