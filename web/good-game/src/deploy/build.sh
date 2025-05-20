#!/bin/sh

set -euxo pipefail

docker build -t isolatedchallengesv4registry.azurecr.io/web/chal2-whitehats:latest ..
docker push isolatedchallengesv4registry.azurecr.io/web/chal2-whitehats:latest
