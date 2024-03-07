
coffee:
	@printf 'Be Happy Even if Things Aren’t Perfect Now. 🎉🎉🎉\n'
	@printf 'Enjoy your coffee! ☕\n'

dev:
	@docker compose -f docker-compose.yaml up --build

run:
	@docker compose -f docker-compose.yaml up --build -d

down:
	@docker compose -f ./docker-compose.yaml down --remove-orphans

shell:
	@docker exec -it geo_stac_fastapi bash

tests:
	@docker exec -it geo_stac_fastapi poetry run pytest

coverage:
	@docker exec -it geo_stac_fastapi poetry run coverage run -m pytest
	@docker exec -it geo_stac_fastapi poetry run coverage report

mypy:
	@docker exec -it geo_stac_fastapi poetry run mypy .

.PHONY: coffee dev run down shell tests coverage mypy
