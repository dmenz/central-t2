#!/bin/bash

cd /home/ubuntu/central-t2

cp frontend/nginx.prod.conf frontend/nginx.conf
cp backend/nginx.prod.conf backend/nginx.conf

# Stop all containers
docker-compose -f docker-compose.prod.yml down
# Build all containers
docker-compose -f docker-compose.prod.yml up -d --build
