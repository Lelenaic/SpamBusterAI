init:
	git clone https://github.com/nomic-ai/gpt4all
	docker compose -f docker-compose.ai.yaml build

cpu:
	docker compose up -d gpt4all

gpu:
	docker compose -f docker-compose.yaml -f docker-compose.ai-gpu.yaml up -d
