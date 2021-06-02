#!/bin/bash

docker container exec compose_tyk_gateway_1 rm -rf /opt/tyk-gateway/middleware/bundles
docker container restart compose_tyk_gateway_1
docker container restart compose_tyk_dashboard_1
sleep 2
./show-ports
docker container logs -f compose_tyk_gateway_1
