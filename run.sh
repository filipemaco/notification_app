#!/usr/bin/env bash
set -e

docker-compose build
docker-compose up -d db
sleep 2
docker-compose up -d notification_service
docker-compose up -d redis
docker-compose up -d celery_worker
docker-compose up -d celery_beat
docker-compose up -d flower

