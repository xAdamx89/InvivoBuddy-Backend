#!/bin/bash


if [ "$1" == "1" ]; then
    # Polacz jako postgres
    sudo docker exec -it db_test psql -U suser -d dev_db

elif [ "$1" == "2" ]; then
    # Polacz jako invivo
    sudo docker exec -it db_test psql -U invivo -d invivo
else
    echo "1 - Polacz jako postgres do bazy testowej postgres"
    echo "2 - Polacz jako invivo do bazy testowej invivo"
fi
