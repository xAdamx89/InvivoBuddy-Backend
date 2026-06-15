from fastapi import APIRouter, Depends, Request
from sqlalchemy import text, select, desc
from sqlalchemy.ext.asyncio import AsyncSession
import crud, schemas, database

from schemas import stmt_data

from crud import dodaj_pomiar, pobierz_liste_danych, dodaj_dane_testowe

from models import TabelePomiarowe

router = APIRouter(
    prefix="/pomiary",
    tags=["Pomiary"]
)

# router.py
@router.put(
            "/pobierz_tablice_pomiarow", 
            response_model=schemas.OdpowiedzLista
        )
async def pobierz_tablice_pomiarow(
    stmt_data: stmt_data,
    db: AsyncSession = Depends(database.get_db),
    current_user: schemas.OdpowiedzJa = Depends(crud.get_current_user)
):
    stmt = (
        select(TabelePomiarowe)
        .where(TabelePomiarowe.owner_id == current_user.id)
        )
    res = db.execute(stmt)
    #dane = res.

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

@router.put("/dodajtestowe")
async def dodaj_dane_testowe_endpoint(
        db: AsyncSession = Depends(database.get_db)
):
    # Dodajemy await, ponieważ funkcja jest async
    await dodaj_dane_testowe(db) 
    return {"status": "Dane testowe zostały dodane"}

