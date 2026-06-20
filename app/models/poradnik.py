from typing import List, TYPE_CHECKING
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

if TYPE_CHECKING:
    from .base_class import Base


class Poradnik(Base):
    __tablename__ = "poradniki"

    PoradnikId: Mapped[int] = mapped_column(primary_key=True, index=True)
    kategoria: Mapped[str] = mapped_column(String(50), nullable=False) # Obserwacje temperatury albo obserwacje śluz
    tytul: Mapped[str] = mapped_column(String(100), nullable=False)
    tresc: Mapped[str] = mapped_column(String(1000), nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
