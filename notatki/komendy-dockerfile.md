# Komendy przy korzystani z Dockerfile

## Zbudowanie obrazu

```bash
docker build -t invivobuddy_api .
```
1. -t invivobuddy_api – Nadajesz swojemu obrazowi przyjazną nazwę (tag).

2. . (kropka na końcu) – Mówi Dockerowi: "znajdź Dockerfile i wszystkie pliki w tym folderze, w którym obecnie jestem".


## Uruchomienie kontenera

```bash
docker run -d --name npr_backend -p 8000:8000 --env-file .env invivobuddy_api
```

1. -d (detach) – Uruchamia aplikację w tle. Dzięki temu nie blokuje Ci terminala.

2. --name npr_backend – Nadajesz działającemu kontenerowi konkretną nazwę, żeby łatwo nim zarządzać.

3. -p 8000:8000 – Łączysz port 8000 na swoim komputerze z portem 8000 wewnątrz kontenera.

4. --env-file .env – Docker wstrzykuje Twoje bezpieczne zmienne (np. hasła do bazy) bezpośrednio do pamięci kontenera.

5. invivobuddy_api – Nazwa obrazu, który zbudowałeś w Kroku 1.

## Krok 3: Codzienne zarządzanie (Kluczowe komendy)
Teraz Twoje FastAPI działa w tle. Jak nad tym zapanować?

### Jak sprawdzić logi i błędy (np. czy FastAPI poprawnie wstało):
```bash
docker logs npr_backend
# (Dodaj flagę -f, czyli docker logs -f npr_backend, jeśli chcesz śledzić logi na żywo, tak jak w normalnym terminalu).
```

### Jak zatrzymać aplikację:
```bash
docker stop npr_backend
```

### Jak ponownie uruchomić zatrzymaną aplikację:
```bash
docker start npr_backend
```

### Jak usunąć kontener (np. żeby postawić czysty od nowa):
```bash
docker rm -f npr_backend
```



```bash

```