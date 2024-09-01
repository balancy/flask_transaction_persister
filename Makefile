all: dev

dev:
	@docker compose up -d --build

prod:
	@docker compose -f docker-compose.yml up -d --build

stop:
	@docker compose down

lint:
	@ruff check src
	@black --check src