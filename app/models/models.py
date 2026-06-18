from typing import List
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, func, Time, Enum, false
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from datetime import datetime
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    UserId: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    email: Mapped[str | None] = mapped_column(String(100), unique=True, index=True, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # POPRAWKA: Czysta relacja dwukierunkowa
    tabele: Mapped[List["TabelePomiarowe"]] = relationship(
        "TabelePomiarowe",
        back_populates="owner",
        cascade="all, delete-orphan"
    )

class Poradnik(Base):
    __tablename__ = "poradnik"

    PoradnikId: Mapped[int] = mapped_column(primary_key=True, index=True)
    kategoria: Mapped[str] = mapped_column(String(50), nullable=False) # Obserwacje temperatury albo obserwacje śluz
    tytul: Mapped[str] = mapped_column(String(100), nullable=False)
    tresc: Mapped[str] = mapped_column(String(1000), nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

class TabelePomiarowe(Base):
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
    owner: Mapped["User"] = relationship("User", back_populates="tabele")
    pomiary: Mapped[List["Pomiary"]] = relationship(
        "Pomiary", back_populates="tabele_pomiarowe", cascade="all, delete-orphan"
    )

class Pomiary(Base):
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

    tabele_pomiarowe: Mapped["TabelePomiarowe"] = relationship(
        "TabelePomiarowe",
        back_populates="pomiary"
    )

