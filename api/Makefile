# Docker Compose Command
DOCKER_COMPOSE = docker-compose

# Define targets and their respective commands
.PHONY: build up down restart clean prune

build:
	$(DOCKER_COMPOSE) build

up:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down

restart:
	$(DOCKER_COMPOSE) restart


clean:
	$(DOCKER_COMPOSE) down -v --remove-orphans


prune:
	docker system prune -af
