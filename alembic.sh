#!/bin/bash

set -e

if [ "$1" == "1" ]; then
    # Plan budowy bazy danych - sprawdza różnice między modelem a bazą danych i generuje migrację
    echo "Generuję nową migrację..."
    alembic revision --autogenerate -m "Auto-migration $(date +%s)"
elif [ "$1" == "2" ]; then
    # Wykonanie migracji
    # Przy ponownym uruchomieniu bazy w RAM
    echo "Stawiam strukturę bazy..."
    alembic upgrade head
    echo "Baza gotowa!"
elif [ "$1" == "3" ]; then
    # Aktualizacja bazy danych gdy zmienie plik models.py
    echo "Generuję nową migrację..."
    alembic revision --autogenerate -m "Auto-migration $(date +%s)"

    echo "Stosuję zmiany w bazie..."
    alembic upgrade head
    echo "Gotowe!"
elif [ "$1" == "4" ]; then
    # Cofnięcie ostatniej zmiany
    alembic downgrade -1
elif [ "$1" == "5" ]; then
    # Sprawdź status migracji alembic
    alembic current
else
    echo "Argumenty:"
    echo "1 - Plan budowy bazy danych - sprawdza różnice między modelem a bazą danych i generuje migrację"
    echo "2 - Wykonanie migracji - Przy ponownym uruchomieniu bazy w RAM"
    echo "3 - wykonaj 1 + 2"
    echo "4 - Cofnięcie ostatniej zmiany"
    echo "5 - Sprawdź status migracji alembic"
fi
