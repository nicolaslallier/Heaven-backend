IMAGE ?= heaven-backend
COMPOSE ?= docker compose

.PHONY: build up down restart logs ps dev clean

build:
	$(COMPOSE) build

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

restart: down up

logs:
	$(COMPOSE) logs -f api

ps:
	$(COMPOSE) ps

dev:
	$(COMPOSE) up --build

clean:
	$(COMPOSE) down --remove-orphans
	docker image rm $(IMAGE) || true
