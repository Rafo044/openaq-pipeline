#!/bin/bash

ACTIVATE_PROCESS_SQL="./var/lib/postgresql/activate_process.sql"

set -a
source ".env"
set +a

docker exec -it pgdata psql -U $POSTGRES_USER -d $POSTGRES_DB -f "$ACTIVATE_PROCESS_SQL"
