#!/bin/bash

ls -la >&2
pwd >&2
whoami >&2


# Stop all containers
docker-compose -f docker-compose.prod.yml down
# Build all containers
docker-compose -f docker-compose.prod.yml up -d --build
