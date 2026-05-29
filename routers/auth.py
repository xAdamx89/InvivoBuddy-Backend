from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import crud, schemas, database, security

router = APIRouter(
    tags=["Uwierzytelnianie i rejestracja"]
)

@router.post("/register", response_model=schemas.OdpowiedzOgolna, status_code=status.HTTP_201_CREATED)
async def register_user(user: schemas.ZadanieRejestracja, db: AsyncSession = Depends(database.get_db)):
    existing_user = await crud.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Użytkownik o tej nazwie już istnieje"
        )
    return await crud.create_user(db=db, user=user)

@router.post("/login", response_model=schemas.OdpowiedzToken)
async def login(login_data: schemas.ZadanieUserLogin, db: AsyncSession = Depends(database.get_db)):
    user = await crud.get_user_by_username(db, login_data.username)
    if not user or not security.verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Błędny login lub hasło lub użytkownik nie istnieje",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = security.create_access_token(data={"sub": user.username})
    return {
        "access_token": access_token,
        "refresh_token": "temporary_refresh_token",
        "token_type": "bearer"
    }
