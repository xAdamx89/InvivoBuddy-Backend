from typing import Optional, Any
from enum import Enum

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

class OdpowiedzOgolna(BaseModel):
    status: str
    resp: Any

class ZadanieDodajPomiar(BaseModel):
    temperatura: float
    data_pomiaru: datetime
    okres: bool

    informacje_dodatkowe: str | None = None

class ZadanieJa(BaseModel):
    id: int
    username: str
    email: EmailStr | None
    created_at: datetime
    avatar_url: str | None
    
    model_config = {"from_attributes": True}

class OdpowiedzJa(BaseModel):
    id: int
    username: str
    email: EmailStr | None
    created_at: datetime
    avatar_url: str | None

    model_config = {"from_attributes": True}

class OdpowiedzPomiar(BaseModel):
    PomiarId: int
    temperatura: float
    data_pomiaru: datetime
    godzina_pomiaru: datetime
    informacje_dodatkowe: str | None
    dzien_cyklu: int

    model_config = {"from_attributes": True}

class OdpowiedzLista(BaseModel):
    status: str
    dane: list[Any]

class stmt_data(BaseModel):
    from_table: str
    where: str

class ZadanieRejestracja(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr | None = None
    password: str = Field(..., min_length=8)
    avatar_url: str | None = None

    class Config:
        from_attributes = True

class ZadanieUserLogin(BaseModel):
    username: str
    password: str

class ZadaniePomiar(BaseModel):
    temperatura: float
    data_pomiaru: str
    okres: Optional[bool] = False
    informacje_dodatkowe: Optional[str] = None

class OdpowiedzToken(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# class ZadaniePomiar(BaseModel):
#     temperatura: float
#     godzina_pomiaru: datetime
#     okres: bool
#     informacje_dodatkowe: str | None = None

class ZadanieWykonajPomiar(BaseModel):
    access_token: str
    pomiar: ZadaniePomiar

class ZadanieZmodyfikujPomiar(BaseModel):
    user_id: int
    godzina_pomiaru: datetime
    informacje_dodatkowe: str | None = None

class ZadanieListaPomiarow(BaseModel):
    pass

class TypObjawuKrwi(str, Enum):
    KRWAWIENIE = "K"
    PLAMIENIE = "P"
    BRUDZENIE = "B"
    BRAK = "N"
