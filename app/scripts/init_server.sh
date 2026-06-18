#!/bin/bash

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
#2. Inicjalizacja (Wersja Async)
#W folderze projektu wykonaj komendę, która stworzy strukturę plików dla projektów asynchronicznych:
alembic init -t async migrations
. ./alembic.sh 2
