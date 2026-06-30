from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db # Zakładam, że masz tę funkcję w database.py
from core.security import oauth2_scheme, SECRET_KEY, ALGORITHM
from jose import jwt
from models.pomiar import User # Import Twojego modelu

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401)
    except:
        raise HTTPException(status_code=401, detail="Nieprawidłowy token")
        
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Użytkownik nie istnieje")
    return user