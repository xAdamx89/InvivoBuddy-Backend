from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import String, Boolean, DateTime, ForeignKey, func, Time, false
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

if TYPE_CHECKING:
    from app.models.base_class import Base


class Pomiar(Base):
    __tablename__ = "pomiary"
    # auto
    pomiar_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tabela_pomiarow_id: Mapped[int] = mapped_column(ForeignKey("tablica_pomiarow.tabela_pomiarowa_id"))
    tabela_pomiarow: Mapped[int] = relationship(back_populates="")

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


