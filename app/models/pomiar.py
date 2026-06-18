from typing import List
from sqlalchemy import String, Boolean, DateTime, ForeignKey, func, Time, false
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.database import Base

class Pomiar(Base):
    __tablename__ = "pomiary"
    # auto
    PomiarId: Mapped[int] = mapped_column(primary_key=True, index=True)

    # KLUCZ OBCY: Wskazuje na konkretny rekord w tabeli_pomiaru
    # Pobrane z bazy
    tabele_pomiarowe_id: Mapped[int] = mapped_column(
        ForeignKey("tabele_pomiarowe.TabelaPomiarowaId"), nullable=False
    )

    # Wylicza z creted_at
    data_pomiaru: Mapped[datetime] = mapped_column(
            DateTime(timezone=True), 
            nullable=True,
            server_default=func.now()
        )
    # Z danych
    temperatura: Mapped[float] = mapped_column(nullable=False)
    # Wylicza z creted_at
    godzina_pomiaru: Mapped[Time] = mapped_column(
            Time, 
            nullable=False
        )
    # auto
    informacje_dodatkowe: Mapped[str | None] = mapped_column(
            String(255), 
            nullable=True
        )
    # auto
    dzien_cyklu: Mapped[int] = mapped_column(nullable=True)

    # auto
    przyjmowanie_progesteronu: Mapped[bool] = mapped_column(
            nullable=True,
            server_default=false()
        )
    
    # auto
    okres: Mapped[Boolean] = mapped_column(
            Boolean,
            server_default=false()
        )
    
    krwawienie_plamienie_brudzenie: Mapped[str | None] = mapped_column(
            nullable=True,
            server_default="BRAK"
        )

    # auto
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    tabele_pomiarowe: Mapped["TabelaPomiarowa"] = relationship(
        "TabelePomiarowe",
        back_populates="pomiary"
    )

