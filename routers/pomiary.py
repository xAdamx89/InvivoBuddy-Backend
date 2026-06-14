from fastapi import APIRouter, Depends, Request
from sqlalchemy import text, select, desc
from sqlalchemy.ext.asyncio import AsyncSession
import crud, schemas, database

from crud import dodaj_pomiar

from models import TabelePomiarowe

router = APIRouter(
    prefix="/pomiary",
    tags=["Pomiary"]
)

# router.py
@router.get("/pobierz", response_model=schemas.OdpowiedzListaPomiarow)
async def pobierz_pomiary(
    db: AsyncSession = Depends(database.get_db),
    current_user: schemas.OdpowiedzJa = Depends(crud.get_current_user)
):
    # Bezpieczne zapytanie SQL przy użyciu bindowania parametrów z SQLAlchemy
    # Filtrujemy automatycznie po ID zalogowanego użytkownika!
    query = """SELECT id, wartosc, data, notatka FROM POMIARY WHERE user_id = :user_id"""
    result = await db.execute(query, {"user_id": current_user.id})
    pomiary = result.fetchall()
    
    # Mapowanie na format odpowiedzi
    lista_pomiarow = [
        schemas.OdpowiedzPomiar(id=p.id, wartosc=p.wartosc, data=str(p.data), notatka=p.notatka) 
        for p in pomiary
    ]
    
    return schemas.OdpowiedzListaPomiarow(status="success", pomiary=lista_pomiarow)    

@router.post("/dodaj", response_model=schemas.OdpowiedzOgolna)
async def dodaj_pomiar_request(
    nowy_pomiar: schemas.ZadanieDodajPomiar,
    request: Request,
    db: AsyncSession = Depends(database.get_db),
    current_user: schemas.OdpowiedzJa = Depends(crud.get_current_user)
):
    user_id = current_user.UserId

    status, resp = await dodaj_pomiar(db, user_id, nowy_pomiar, True)

    if status != 0:
        return {"status": f"{resp}"}
    else:
        return {"status": "OK"}

@router.put("/zmodyfikuj", response_model=schemas.OdpowiedzOgolna)
async def zmodyfikuj_pomiar(
    response: schemas.ZadanieZmodyfikujPomiar, 
    db: AsyncSession = Depends(database.get_db)
):
    pass