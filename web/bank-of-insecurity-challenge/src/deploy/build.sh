#!/bin/sh

set -euxo pipefail

docker build -t isolatedchallengesv4registry.azurecr.io/web/sql-injection:latest ..
docker push isolatedchallengesv4registry.azurecr.io/web/sql-injection:latest
