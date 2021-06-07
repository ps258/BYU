# Python plugin development notes


## Steps to setup the enviornment.

### Create the containers
```bash
docker-compose up -d
```

This creates:
- compose_redis_1
- compose_mongo_1
- compose_tyk_dashboard_1
- compose_tyk_gateway_1
- compose_tyk_build_1 to build the bundles and serve them to compose_tyk_gateway_1

### Install a dashboard licence and setup some mock APIs.
This demo doesn't provide the API but the bundles will be called register.zip and auth.zip

### Update compose_tyk_build_1 to have the tools needed
```bash
docker container exec compose_tyk_build_1 apt-get update
docker container exec compose_tyk_build_1 apt-get install zip unzip -qy
docker container exec compose_tyk_build_1 /root/plugin/mkvendor.sh
```

### Build and serve the plugins
```bash
docker container exec -it compose_tyk_build_1 /root/plugin/build.sh
```

### Cycle the gateway and dashboard to pull in the bundles
```bash
./publish
```