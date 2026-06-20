from __future__ import annotations
from typing import List, TYPE_CHECKING
from sqlalchemy import String, DateTime, ForeignKey, func, Time, false
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .base_class import Base

if TYPE_CHECKING:
    from .pomiar import Pomiar


class TabelaPomiarowa(Base):
    __tablename__ = "tabele_pomiarowe"

    tabela_pomiarowa_id: Mapped[int] = mapped_column(
            primary_key=True, 
            index=True
        )
    # Właściciel tabeli z pomiarami
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    owner: Mapped["TabelaPomiarowa"] = relationship(back_populates="tabela_pomiarowa_id")
    # Pomiary w tablicy pomiarow
    pomiary_id: Mapped[List["Pomiar"]] = relationship(back_populates="parent", cascade="all, delete")



    imie_i_nazwisko: Mapped[str] = mapped_column(String(100), nullable=True)
    wiek: Mapped[int] = mapped_column(nullable=True)
    godzina_pomiaru: Mapped[Time] = mapped_column(Time, nullable=True)
    rok: Mapped[int] = mapped_column(nullable=True)
    numer_cyklu: Mapped[int] = mapped_column(nullable=True)
    pierwszy_dzien_miesiaczki: Mapped[int] = mapped_column(nullable=True)
    dlugosc_cyklu: Mapped[int] = mapped_column(nullable=True)
    dlugosc_fazy_lutealnej: Mapped[int] = mapped_column(nullable=True)
    informacje_dodatkowe: Mapped[str | None] = mapped_column(String(255), nullable=True)
    koniec_cyklu: Mapped[bool] = mapped_column(
            nullable=False,
            server_default=false()
        )

    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
