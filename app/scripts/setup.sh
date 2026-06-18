#!/bin/bash

echo "Skrypt do ustawień środowiskowych projektu."

while :
do
    wyjdz=0
    read -p "Wybierz tryp pracy: DEV (Na urządzeniu), PROD (Przez sieć LAN). Wpisz '0' aby wyjść:  " odpowiedz
    if [ "$odpowiedz" == "DEV" ]; then
        sed -i "s/APP_MODE=.*/APP_MODE='DEV'/" .env
        echo "ZMieniono środowisko na DEV."
        wyjdz=1
    elif [ "$odpowiedz" == "PROD" ]; then
        sed -i "s/APP_MODE=.*/APP_MODE='PROD'/" .env
        echo "Zmieniono środowisko na PROD."
        wyjdz=1
    elif [ $odpowiedz -eq 0 ]; then
        echo "Zamykanie..."
        exit 0
    else
        echo "Nie rozpoznano argumentu. Podaj: DEV, PROD lub 0."
    fi

    if [ $wyjdz -eq 1 ]; then
        break
    fi
done
