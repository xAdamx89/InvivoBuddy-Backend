# User potrzebuje takich pozwoleń w bazie danych do obsługi alembic i pełnego dostępu do bazy danych
```
-- 1. Pozwól użytkownikowi łączyć się z bazą
GRANT CONNECT ON DATABASE invivobuddy_db TO invivobuddy;

-- 2. Pozwól mu widzieć i używać schematu public
GRANT USAGE ON SCHEMA public TO invivobuddy;

-- 3. Pozwól mu tworzyć nowe tabele (potrzebne dla Alembica)
GRANT CREATE ON SCHEMA public TO invivobuddy;

-- 4. Ustaw go jako właściciela schematu (najbezpieczniejsza opcja dla migracji)
ALTER SCHEMA public OWNER TO invivobuddy;

-- 5. Opcjonalnie: Ustaw go jako właściciela całej bazy
ALTER DATABASE invivobuddy_db OWNER TO invivobuddy;
```
