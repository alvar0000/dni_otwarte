from datetime import datetime, timedelta
from jose import JWTError, jwt
from . import schemas, database
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from .repository.stand import get_user_with_phone_nr

SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f44caa6cf63b88e8d3e7'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


# Generowanie tokenu JWT
def create_access_token(data: dict):
    to_encode = data.copy()

    # Godzina, o której token straci ważność
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# Weryfikacja tokenu i uzyskanie aktualnego użytkownika
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        phone_nr: str = payload.get('sub')
        if phone_nr is None:
            raise JWTError("Invalid sub claim")
        token_data = schemas.TokenData(phone_nr=phone_nr)
        return token_data
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {e}",
            headers={'WWW-Authenticate': "Bearer"}
        )
