#!/bin/bash
echo "Rozpoczynam łączenie z bazą danych psql..."
sudo docker exec -it db_dev psql -U invivo -d invivo
