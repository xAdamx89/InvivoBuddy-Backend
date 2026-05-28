from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import crud, schemas, database

router = APIRouter(
    prefix="/pomiary",
    tags=["Pomiary"]
)

@router.post("/pobierz", response_model=schemas.OdpowiedzListaPomiarow)
async def pobierz_pomiary(
    pobierz_pomiary: schemas.ZadanieListaPomiarow,
    db: AsyncSession = Depends(database.get_db),
    current_user: schemas.OdpowiedzJa = Depends(crud.get_current_user)
):
    pass

@router.post("/dodaj", response_model=schemas.OdpowiedzOgolna)
async def dodaj_pomiar(
    nowy_pomiar: schemas.ZadanieDodajPomiar,
    db: AsyncSession = Depends(database.get_db),
    current_user: schemas.OdpowiedzJa = Depends(crud.get_current_user)
):
    pass

@router.put("/zmodyfikuj", response_model=schemas.OdpowiedzOgolna)
async def zmodyfikuj_pomiar(
    response: schemas.ZadanieZmodyfikujPomiar, 
    db: AsyncSession = Depends(database.get_db)
):
    pass