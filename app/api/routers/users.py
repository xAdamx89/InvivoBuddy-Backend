from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import repositories.crud as crud, schemas.schemas as schemas, db.database as database

router = APIRouter(
    prefix="/users",
    tags=["Użytkownicy"]
)

@router.get("/me", response_model=schemas.OdpowiedzJa)
async def read_users_me(
    pobierz_me: schemas.ZadanieJa,
    db: AsyncSession = Depends(database.get_db),
    current_user: schemas.OdpowiedzJa = Depends(crud.get_current_user)
):
    return current_user