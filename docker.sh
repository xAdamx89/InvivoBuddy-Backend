#!/bin/bash

set -e

if [ "$1" == "1" ]; then
    # Budowa obrazu z Dockerfile (bez uruchomienia)
    echo "Buduję obraz dockera..."
    sudo docker build -t npr_backend .
elif [ "$1" == "2" ]; then
    # Uruchomienie kontenera
    echo "Uruchamiam kontener z obrazem npr_backend..."
    sudo docker run -d --name invivobuddy_api -p 8000:8000 --env-file .env npr_backend:latest
elif [ "$1" == "3" ]; then
    # Sprawdz logi kontenera invivobuddy_api
    echo "Uruchamiam logi kontenera..."
    docker logs invivobuddy_api
else
    echo "Argumenty:"
    echo "1 - Budowa obrazu z Dockerfile (bez uruchomienia)"
    echo "2 - Uruchomienie kontenera invivobuddy_api z obrazu npr_backend:latest."
    echo "3 - Sprawdz logi kontenera invivobuddy_api."

fi


# Komendy przy korzystani z Dockerfile


### Jak zatrzymać aplikację:
#```bash
#docker stop npr_backend
#```

### Jak ponownie uruchomić zatrzymaną aplikację:
#```bash
#docker start npr_backend
#```

### Jak usunąć kontener (np. żeby postawić czysty od nowa):
#```bash
#docker rm -f npr_backend
#```
