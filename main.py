from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordBearer

# Importujemy nasze nowe routery
from routers import auth, users, pomiary

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI(title="InvivoBuddy API")

# --- Globalne Exception Handlery (zostają w main) ---

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"BŁĄD KRYTYCZNY: {exc}")
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


# --- Dołączanie routerów do aplikacji ---
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(pomiary.router)


# Prosty testowy endpoint
@app.get("/")
async def root():
    return {"message": "InvivoBuddy API is running"}


if __name__ == "__main__":
    import uvicorn
    # host 0.0.0.0 ułatwia testowanie aplikacji bezpośrednio z telefonu z Androidem
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)