import os
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import models, schemas, security
from sqlalchemy import select, desc, insert

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError  # lub od firmy jose: from jose import jwt, JWTError
from database import get_db
import schemas
from models import TabelePomiarowe, Pomiary

from datetime import datetime, timedelta, time

from utils.utils import round_time_to_half_hour

load_dotenv()  # Ładuje zmienne środowiskowe z pliku .

# Te zmienne powinny być takie same jak w Twoim module security!
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def najmlodsza_tabelepomiarowe(db: AsyncSession, user_id):
    """Funkcja do pobrania najmłodszej TabelaPomiarowa."""
    stmt = (
        select(TabelePomiarowe)
        .where(TabelePomiarowe.owner_id == user_id)
        .order_by(desc(TabelePomiarowe.created_at))
        .limit(1)
    )
    resp = await db.execute(stmt)
    dane = resp.scalar_one_or_none()

    return dane

async def utworz_tabelepomiarowe_dodaj_pomiar(db: AsyncSession, db_pomiar, user_id, dane_najmlodszej_tabelipomiarow, test):
    dane = dane_najmlodszej_tabelipomiarow

    dt_from_request = db_pomiar.data_pomiaru
    zaokraglony_dt = round_time_to_half_hour(dt_from_request)

    stmt = (
        insert(TabelePomiarowe)
        .values(
            owner_id = user_id,
            godzina_pomiaru = zaokraglony_dt,
            koniec_cyklu = False
        )
    )
    try:
        result = await db.execute(stmt)
        await db.commit()
    except Exception as e:
        await db.rollback()
        print(f"Błąd zapisu do bazy: {e}")
        raise

    dane = await najmlodsza_tabelepomiarowe(db, user_id)

    await dodaj_pomiar_crud(db, db_pomiar, user_id, dane, zaokraglony_dt)

async def dodaj_pomiar_crud(db: AsyncSession, db_pomiar, user_id, dane_najmlodszej_tabelipomiarow, zaokraglony_dt):
    dane = dane_najmlodszej_tabelipomiarow
    stmt = (
        insert(Pomiary)
        .values(
            tabela_pomiaru_id = dane.TabelaPomiarowaId,
            temperatura = db_pomiar.temperatura,
            godzina_pomiaru = zaokraglony_dt,
            okres = db_pomiar.okres
        )
    )
    try:
        result = await db.execute(stmt)
        await db.commit()
    except Exception as e:
        await db.rollback()
        print(f"\n\nBłąd zapisu do bazy: {e}\n\n")
        raise

    return 'OK'

async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: AsyncSession = Depends(get_db)
) -> models.User:
    
    # Tworzymy generyczny błąd, który wyrzucimy, jeśli token będzie zły
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Nie można zweryfikować uprawnień (zły lub wygasły token)",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 1. Odkodowujemy token JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # 2. Wyciągamy nazwę użytkownika (zaszytą pod kluczem "sub" podczas logowania)
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
            
    except Exception: # Tutaj złapie np. ExpiredSignatureError jeśli token wygasł
        raise credentials_exception
        
    # 3. Szukamy użytkownika w bazie danych na podstawie nazwy z tokenu
    user = await get_user_by_username(db, username=username)
    
    if user is None:
        raise credentials_exception
        
    # 4. Jeśli wszystko jest ok, zwracamy obiekt użytkownika
    return user

async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(models.User).filter(models.User.username == username))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: schemas.ZadanieRejestracja):
    # 1. Haszujemy hasło z security.py
    hashed_pwd = security.hash_password(user.password)
    
    # 2. Tworzymy obiekt modelu
    db_user = models.User(
        username=user.username,
        email=user.email,
        avatar_url=user.avatar_url,
        hashed_password=hashed_pwd
    )
    
    # 3. Zapisujemy w bazie
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def dodaj_pomiar(db: AsyncSession, user_id: int, pomiar_data: schemas.ZadanieDodajPomiar, test: bool = False):
    # Tworzymy obiekt modelu SQLAlchemy na podstawie danych ze schematu Pydantic
    db_pomiar = models.Pomiary(
        temperatura=pomiar_data.temperatura,
        data_pomiaru=pomiar_data.data_pomiaru,
        okres=pomiar_data.okres,
        informacje_dodatkowe=pomiar_data.informacje_dodatkowe
    )

    dt_from_request = db_pomiar.data_pomiaru
    zaokraglony_dt = round_time_to_half_hour(dt_from_request)
    
    dane_najmlodszej_tabelipomiarow = await najmlodsza_tabelepomiarowe(db, user_id)

    # Jeżeli nie ma tablicy wpisów temperatur albo najmłodsza tablica jest zamknięta, to zakłada nową i do niej wpisuje.
    if dane_najmlodszej_tabelipomiarow is None or dane_najmlodszej_tabelipomiarow.koniec_cyklu is True:
        await utworz_tabelepomiarowe_dodaj_pomiar(db, db_pomiar, user_id, dane_najmlodszej_tabelipomiarow, test)
    # Jeżeli tablica istnieje i nie jest zamknięta
    elif dane_najmlodszej_tabelipomiarow.koniec_cyklu is False:
        stmt = (
            select(Pomiary)
            .where(Pomiary.tabela_pomiaru_id == dane_najmlodszej_tabelipomiarow.TabelaPomiarowaId)
        )
        resp = await db.execute(stmt)
        dane = resp.scalar_one_or_none()

        if dane is not None:
            return 1 , 'Er: Pomiar już wpisany'
        else:
            dodaj_pomiar_crud(db, db_pomiar, user_id, dane_najmlodszej_tabelipomiarow, zaokraglony_dt)

    return 0, 'OK'

async def sprawdz_tablica_pomiarow(user_id):
    pass


