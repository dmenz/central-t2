#!/bin/bash

cd /home/ubuntu/central-t2

# Stop all containers
docker-compose -f docker-compose.prod.yml down
# Build all containers
docker-compose -f docker-compose.prod.yml up -d --build
