from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import RequestValidationError, ResponseValidationError

# Importujemy nasze nowe routery
from app.routers import pomiary
from app.routers import users
from app.routers import auth

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI(title="InvivoBuddy API")

# --- JEDNOZNACZNE I GLOBALNE EXCEPTION HANDLERY ---

@app.exception_handler(RequestValidationError)
async def global_request_validation_handler(request: Request, exc: RequestValidationError):
    print("\n❌ [GLOBALNY CATCH] Błąd walidacji danych wejściowych (Request):")
    print(exc.errors())
    print("----------------------------------------------------------------\n")
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "message": "Dane przesłane z telefonu nie pasują do modelu schematu.",
            "details": exc.errors()
        }
    )

@app.exception_handler(ResponseValidationError)
async def global_response_validation_handler(request: Request, exc: ResponseValidationError):
    print("\n❌ [GLOBALNY CATCH] Błąd walidacji odpowiedzi (Response):")
    print(exc.errors())
    print("----------------------------------------------------------------\n")
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Serwer wygenerował odpowiedź w niepoprawnym formacie.",
            "details": exc.errors()
        }
    )

@app.exception_handler(TypeError)
async def json_type_error_handler(request: Request, exc: TypeError):
    print(f"❌ [GLOBALNY CATCH] Błąd typu/serializacji JSON: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Serwer próbował przetworzyć lub zwrócić dane w nieobsługiwanym formacie."
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"💥 BŁĄD KRYTYCZNY SERWERA: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Wystąpił nieoczekiwany błąd serwera.",
            "details": str(exc)
        }
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