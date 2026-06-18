from typing import List
from sqlalchemy import String, DateTime, ForeignKey, func, Time, false
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.database import Base

class TabelaPomiarowa(Base):
    __tablename__ = "tabele_pomiarowe"

    TabelaPomiarowaId: Mapped[int] = mapped_column(primary_key=True, index=True)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.UserId", ondelete="CASCADE"), nullable=False)
    user_id_udostepnione: Mapped[int | None] = mapped_column(nullable=True)

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

    # RELACJE
    owner: Mapped["user"] = relationship("User", back_populates="tabele")
    pomiary: Mapped[List["Pomiar"]] = relationship(
        "Pomiary", back_populates="tabele_pomiarowe", cascade="all, delete-orphan"
    )