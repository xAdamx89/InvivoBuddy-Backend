from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker 
from sqlalchemy.orm import declarative_base
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("CONN_STR")

engine = create_async_engine(DATABASE_URL, echo=True)

# Fabryka sesji
AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    expire_on_commit=False
)

Base = declarative_base()

# Dependency - to wstrzykniemy do endpointów FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def test_connection():
    print("--- Rozpoczynam test połączenia asynchronicznego ---")
    try:
        # Próba otwarcia sesji i wykonania prostego zapytania
        async with engine.connect() as conn:
            # W asyncpg używamy text() tak samo jak w zwykłym SQLAlchemy
            from sqlalchemy import text
            result = await conn.execute(text("SELECT current_database(), current_user;"))
            db_info = result.fetchone()
            print(f"✅ Sukces!")
            print(f"Baza: {db_info[0]}")
            print(f"Użytkownik: {db_info[1]}")
            
    except Exception as e:
        print(f"❌ Błąd połączenia!")
        print(f"Szczegóły: {e}")
    finally:
        # Zamykamy silnik, aby nie "wisiał" w terminalu
        await engine.dispose()

if __name__ == "__main__":
    # Uruchomienie asynchronicznej funkcji testowej
    asyncio.run(test_connection())