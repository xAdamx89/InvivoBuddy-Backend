from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from models import Pomiary
class OdpowiedzOgolna(BaseModel):
    response: str

class ZadanieJa(BaseModel):
    id: int
    username: str
    email: EmailStr | None
    created_at: datetime

class OdpowiedzJa(BaseModel):
    id: int
    username: str
    email: EmailStr | None
    created_at: datetime
    avatar_url: str | None

    model_config = {"from_attributes": True}

# To wysyła Android przy rejestracji
class ZadanieRejestracja(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr | None = None
    password: str = Field(..., min_length=8)
    avatar_url: str | None = None

class ZadanieUserLogin(BaseModel):
    username: str
    password: str

# To wysyła Serwer do Androida (nigdy nie wysyłamy hasła!)
class OdpowiedzUser(BaseModel):
    id: int
    username: str
    email: EmailStr | None
    created_at: datetime
    avatar_url: str | None
    
    model_config = {"from_attributes": True}




class OdpowiedzToken(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"



class ZadanieWykonajPomiar(BaseModel):
    access_token: str
    pomiar: Pomiary

    model_config = ConfigDict(arbitrary_types_allowed=True)


class ZadanieDodajPomiar(BaseModel):
    imie_i_nazwisko: str
    wiek: int
    godzina_pomiaru: datetime
    rok: int
    numer_cyklu: int
    pierwszy_dzien_miesiaczki: int
    dlugosc_cyklu: int
    dlugosc_fazy_lutealnej: int
    informacje_dodatkowe: str | None = None

class ZadanieZmodyfikujPomiar(BaseModel):
    pass

class OdpowiedzZmodyfikujPomiar(BaseModel):
    pass

class ZadanieListaPomiarow(BaseModel):
    pass
class OdpowiedzListaPomiarow(BaseModel):
    pass
