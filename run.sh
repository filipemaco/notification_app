#!/usr/bin/env bash
set -e

docker-compose build
docker-compose up -d db
sleep 2
docker-compose up notification_service
docker-compose up -d

