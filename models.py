from typing import List
from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    # Mapped i mapped_column dają lepsze wsparcie dla podpowiadania składni (IDE)
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    email: Mapped[str | None] = mapped_column(String(100), unique=True, index=True, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    # server_default=func.now() sprawia, że to PostgreSQL wstawi datę
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )

class poradnik(Base):
    __tablename__ = "poradnik"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    kategoria: Mapped[str] = mapped_column(String(50), nullable=False) # Obserwacje temperatury albo obserwacje śluz
    tytul: Mapped[str] = mapped_column(String(100), nullable=False)
    tresc: Mapped[str] = mapped_column(String(255), nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )

class TabelePomiarowe(Base):
    __tablename__ = "tabela_pomiaru"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    owner_id: Mapped[int] = mapped_column(nullable=False)
    user_id_udostepnione: Mapped[int | None] = mapped_column(nullable=True)
    # pomiar_id: Mapped[int] = mapped_column(nullable=False)

    imie_i_nazwisko: Mapped[str] = mapped_column(String(100), nullable=False)
    wiek: Mapped[int] = mapped_column(nullable=False)
    godzina_pomiaru: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    rok: Mapped[int] = mapped_column(nullable=False)
    numer_cyklu: Mapped[int] = mapped_column(nullable=False)
    pierwszy_dzien_miesiaczki: Mapped[int] = mapped_column(nullable=False)
    dlugosc_cyklu: Mapped[int] = mapped_column(nullable=False)
    dlugosc_fazy_lutealnej: Mapped[int] = mapped_column(nullable=False)
    informacje_dodatkowe: Mapped[str | None] = mapped_column(String(255), nullable=True)

    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )

    # RELACJA: Lista wszystkich pomiarów przypisanych do tej tabeli
    pomiary: Mapped[List["Pomiary"]] = relationship(
        back_populates="tabela_matka", 
        cascade="all, delete-orphan" # Jeśli usuniesz tabelę, usuną się też pomiary
    )

class Pomiary(Base):
    __tablename__ = "pomiary"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # KLUCZ OBCY: Wskazuje na konkretny rekord w tabeli_pomiaru
    id_tabeli_pomiaru: Mapped[int] = mapped_column(
        ForeignKey("tabela_pomiaru.id"), nullable=False
    )

    id_tabeli_pomiaru: Mapped[int] = mapped_column(nullable=False)
    data_pomiaru: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    temperatura: Mapped[float] = mapped_column(nullable=False)
    godzina_pomiaru: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    informacje_dodatkowe: Mapped[str | None] = mapped_column(String(255), nullable=True)
    dzien_cyklu: Mapped[int] = mapped_column(nullable=False)

    przyjmowanie_progesteronu: Mapped[bool] = mapped_column(nullable=False)
    
    krwawienie_plamienie_brudzenie: Mapped[str] = mapped_column(String(1), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
