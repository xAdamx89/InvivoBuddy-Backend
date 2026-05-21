import os
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import models, schemas, security

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError  # lub od firmy jose: from jose import jwt, JWTError
from database import get_db
import schemas
import models # Zakładam, że tak nazywa się Twój plik z modelami bazy danych

load_dotenv()  # Ładuje zmienne środowiskowe z pliku .

# Te zmienne powinny być takie same jak w Twoim module security!
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

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