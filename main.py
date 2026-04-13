from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.ext.asyncio import AsyncSession
import crud, schemas, database
import security

app = FastAPI(title="InvivoBuddy API")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Tutaj logujesz błąd w konsoli serwera (na Debianie)
    print(f"BŁĄD KRYTYCZNY: {exc}")
    
    # Zwracasz ładnego JSON-a do Androida
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Wystąpił nieoczekiwany błąd serwera.",
            "details": str(exc) if app.debug else "Skontaktuj się z administratorem"
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": "Błędne dane wejściowe", "params": exc.errors()}
    )

# Rejestracja użytkownika
@app.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: schemas.UserCreate, db: AsyncSession = Depends(database.get_db)):
    # 1. Sprawdź czy user już istnieje (po username)
    existing_user = await crud.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Użytkownik o tej nazwie już istnieje"
        )
    
    # 2. Tworzenie użytkownika w bazie
    return await crud.create_user(db=db, user=user)

@app.post("/login", response_model=schemas.TokenResponse)
async def login(login_data: schemas.UserLoginRequest, db: AsyncSession = Depends(database.get_db)):
    # 1. Pobierz użytkownika z bazy
    user = await crud.get_user_by_username(db, login_data.username)
    
    # 2. Sprawdź czy user istnieje i czy hasło jest poprawne
    if not user or not security.verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Błędny login lub hasło lub użytkownik nie istnieje",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Wygeneruj tokeny
    access_token = security.create_access_token(data={"sub": user.username})
    
    # Dla uproszczenia na razie dajemy ten sam token jako refresh lub pusty string
    return {
        "access_token": access_token,
        "refresh_token": "temporary_refresh_token",
        "token_type": "bearer"
    }

# Prosty testowy endpoint
@app.get("/")
async def root():
    return {"message": "InvivoBuddy API is running"}

if __name__ == "__main__":
    import uvicorn
    # host 0.0.0.0 pozwala na dostęp z innych urządzeń w sieci (np. z Twojego Androida)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)