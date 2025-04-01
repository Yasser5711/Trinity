#!/bin/bash

docker rm -f $(docker ps -a -q);docker volume rm $(docker volume ls -q)
sudo rm -r ./back/__pycache__/ ./back/alembic/__pycache__/ ./back/alembic/versions/*.py back/db/__pycache__/ back/api/__pycache__/ back/core/__pycache back/db/schemas/__pycache__ back/db/models/__pycache__  back/core/__pycache__ back/core/helpers/__pycache__ back/alembic/versions/__pycache__
docker compose -f docker-compose-dev.yml --profile front --profile back up --build