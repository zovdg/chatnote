
ifeq ($(UNAME),Darwin)
	RM=rm -dRf
else
	RM=rm -rf
endif

build:
	docker-compose build

# db commands:
db-init:
	docker-compose exec backend aerich init -t src.db.config.TORTOISE_ORM
	docker-compose exec backend aerich init-db

db-un-init:
	${RM} services/backend/migrations
	${RM} services/backend/pyproject.toml

db-migrate:
	docker-compose exec backend aerich migrate
	docker-compose exec backend aerich upgrade

db-use:
	docker-compose exec db psql -U chatnote -w chatnote -d chatnote

# service commands:
service-restart: service-stop service-start

service-start:
	docker-compose up -d

service-stop:
	docker-compose kill



