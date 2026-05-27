.PHONY: help install dev test lint format clean docker-up docker-down migrate migrate-create setup security

BACKEND_DIR := backend
UV := uv
BACKEND_CLEAN_DIRS := .pytest_cache coverage htmlcov .mypy_cache .ruff_cache

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:   ## Install dependencies
	cd $(BACKEND_DIR) && $(UV) sync

dev:  ## Run development server
	cd $(BACKEND_DIR) && $(UV) run python manage.py runserver

test:  ## Run tests
	cd $(BACKEND_DIR) && $(UV) run pytest -v

lint:  ## Run linting
	cd $(BACKEND_DIR) && $(UV) run ruff check .
	cd $(BACKEND_DIR) && $(UV) run mypy .

format:   ## Format code
	cd $(BACKEND_DIR) && $(UV) run ruff format .

clean:  ## Clean cache files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf $(addprefix $(BACKEND_DIR)/,$(BACKEND_CLEAN_DIRS))

docker-up:  ## Start Docker containers
	docker compose up --build -d

docker-down:  ## Stop Docker containers
	docker compose down

migrate:  ## Run database migrations
	cd $(BACKEND_DIR) && $(UV) run python manage.py migrate

migrate-create:  ## Create new migration
	cd $(BACKEND_DIR) && $(UV) run python manage.py makemigrations $(app)

setup:  ## Reset and load fixtures
	cd $(BACKEND_DIR) && $(UV) run python manage.py setup

security:  ## Run security checks
	cd $(BACKEND_DIR) && $(UV) run bandit -r apps/ -c pyproject.toml
	cd $(BACKEND_DIR) && $(UV) run pip-audit || true
