#!/bin/bash

if [ "$1" == "1" ]; then
    # Plan budowy bazy danych - sprawdza różnice między modelem a bazą danych i generuje migrację
    alembic revision --autogenerate -m "Initial migration"
elif [ "$1" == "2" ]; then
    # Wykonanie migracji
    alembic upgrade head
elif [ "$1" == "3" ]; then
    alembic revision --autogenerate -m "Initial migration"
    alembic upgrade head
elif [ "$1" == "4" ]; then
    # Cofnięcie ostatniej zmiany
    alembic downgrade -1
else
    echo "Argumenty:"
    echo "1 - Plan budowy bazy danych - sprawdza różnice między modelem a bazą danych i generuje migrację"
    echo "2 - Wykonanie migracji"
    echo "3 - wykonaj 1 + 2"
    echo "4 - Cofnięcie ostatniej zmiany"
fi
