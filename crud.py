from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import models, schemas, security

async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(models.User).filter(models.User.username == username))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
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