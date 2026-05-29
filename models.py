from typing import List
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, func, Time, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from datetime import datetime
from database import Base

from models_enum import TypObjawuKrwi

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
    __tablename__ = "tabela_pomiaru"

    TabelaPomiarowaId: Mapped[int] = mapped_column(primary_key=True, index=True)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.UserId", ondelete="CASCADE"), nullable=False)
    user_id_udostepnione: Mapped[int | None] = mapped_column(nullable=True)

    imie_i_nazwisko: Mapped[str] = mapped_column(String(100), nullable=False)
    wiek: Mapped[int] = mapped_column(nullable=False)
    godzina_pomiaru: Mapped[Time] = mapped_column(Time, nullable=False)
    rok: Mapped[int] = mapped_column(nullable=False)
    numer_cyklu: Mapped[int] = mapped_column(nullable=False)
    pierwszy_dzien_miesiaczki: Mapped[int] = mapped_column(nullable=False)
    dlugosc_cyklu: Mapped[int] = mapped_column(nullable=False)
    dlugosc_fazy_lutealnej: Mapped[int] = mapped_column(nullable=False)
    informacje_dodatkowe: Mapped[str | None] = mapped_column(String(255), nullable=True)
    koniec_cyklu: Mapped[bool] = mapped_column(nullable=False)

    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # RELACJE
    owner: Mapped["User"] = relationship("User", back_populates="tabele")
    pomiary: Mapped[List["Pomiary"]] = relationship(
        "Pomiary", back_populates="tabela_pomiaru", cascade="all, delete-orphan"
    )
class Pomiary(Base):
    __tablename__ = "pomiary"

    PomiarId: Mapped[int] = mapped_column(primary_key=True, index=True)

    # KLUCZ OBCY: Wskazuje na konkretny rekord w tabeli_pomiaru
    tabela_pomiaru_id: Mapped[int] = mapped_column(
        ForeignKey("tabela_pomiaru.TabelaPomiarowaId"), nullable=False
    )

    data_pomiaru: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    temperatura: Mapped[float] = mapped_column(nullable=False)
    godzina_pomiaru: Mapped[Time] = mapped_column(Time, nullable=False)
    informacje_dodatkowe: Mapped[str | None] = mapped_column(String(255), nullable=True)
    dzien_cyklu: Mapped[int] = mapped_column(nullable=False)

    przyjmowanie_progesteronu: Mapped[bool] = mapped_column(nullable=False)
    
    krwawienie_plamienie_brudzenie: Mapped[TypObjawuKrwi] = mapped_column(Enum(TypObjawuKrwi), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    tabela_pomiaru: Mapped["TabelePomiarowe"] = relationship(
        "TabelePomiarowe",
        back_populates="pomiary"
    )
