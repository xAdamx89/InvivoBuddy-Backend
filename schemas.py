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
    avatar_url: str | None
    
    model_config = {"from_attributes": True}
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





class OdpowiedzToken(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"



class ZadanieWykonajPomiar(BaseModel):
    access_token: str
    pomiar: Pomiary

    model_config = ConfigDict(arbitrary_types_allowed=True)


class ZadanieDodajPomiar(BaseModel):
    user_id: int
    godzina_pomiaru: datetime
    okres: bool

    informacje_dodatkowe: str | None = None

class ZadanieZmodyfikujPomiar(BaseModel):
    user_id: int
    godzina_pomiaru: datetime
    informacje_dodatkowe: str | None = None

class ZadanieListaPomiarow(BaseModel):
    pass
class OdpowiedzListaPomiarow(BaseModel):
    pass
