#!/bin/bash

set -e

if [ "$1" == "1" ]; then
    # Plan budowy bazy danych - sprawdza różnice między modelem a bazą danych i generuje nowy plik migracji
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
elif [ "$1" == "6" ]; then
    # Zapomnięcie aktualnej nie zamkniętej migracji
    alembic stamp base
elif [ "$1" == "7" ]; then
    # Zresetuj całą wersje alembic
    read -p "Czy na pewno chcesz zresetować historie wersji migracji alembic? (./migrations/versions/) (Y/n): " decyzja
    if [ "$decyzja" == "Y" ]; then
        rm migrations/versions/*.py
        alembic revision --autogenerate -m "reset"
        alembic upgrade head
    fi

else
    echo "Argumenty:"
    echo "1 - Sprawdza różnice między modelem a bazą danych i generuje nowy plik migracji"
    echo "2 - Wykonanie migracji - Przy ponownym uruchomieniu bazy w RAM."
    echo "    Alembic wchodzi do bazy danych, patrzy na plik migracji i sam wykonuje potrzebny kod SQL."
    echo "3 - wykonaj 1 + 2"
    echo "4 - Cofnięcie ostatniej zmiany"
    echo "5 - Sprawdź status migracji alembic"
    echo "6 - Zapomnięcie aktualnej nie zamkniętej migracji"
    echo "7 - Zresetuj całą wersje alembic"
fi
