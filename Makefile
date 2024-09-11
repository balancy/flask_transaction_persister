all: dev

dev:
	@docker compose up -d --build --remove-orphans

prod:
	@docker compose -f docker-compose.yml up -d --build --remove-orphans

stop:
	@docker compose down

load:
	@docker compose -f docker-compose.load.yml up -d --build --remove-orphans

lint:
	@ruff check .
	@black --check src

test:
	@docker exec transaction-app pytest