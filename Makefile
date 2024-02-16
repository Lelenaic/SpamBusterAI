init:
	rm -rf gpt4all
	git clone https://github.com/nomic-ai/gpt4all
	docker compose build

cpu:
	docker compose up -d gpt4all

gpu:
	docker compose -f docker-compose.yaml -f docker-compose.ai-gpu.yaml up -d
