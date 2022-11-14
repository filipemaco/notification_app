format:
	black --line-length 120 .
	isort .

clean-docker:
	docker-compose down -v

clean-venv:
	rm -rf venv


clean: clean-docker clean-venv
