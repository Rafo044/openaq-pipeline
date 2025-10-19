.PHONY: up down logs start stop main
include .env
export

up:
	docker compose up -d --build

down:
	docker compose down --volumes

logs:
	docker compose logs

start:
	docker compose start


stop:
	docker compose stop

init:
	sudo chmod +x script/init.sh
	./script/init.sh

main:
	sudo mkdir -p logs
	sudo chmod 777 logs/
	docker exec -it parser python main.py

activate_process:
	sudo chmod 777 acivate_log.sh
	./script/acivate_process.sh

ps:
	docker compose ps

run:
	docker exec -it datalineage npm run dev

test:
	pytest tests/test_main.py
