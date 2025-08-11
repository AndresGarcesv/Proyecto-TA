from datetime import datetime, timedelta
from typing import Optional
import os
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from models import Profesora
from passlib.context import CryptContext

# Configuración desde .env
SECRET_KEY = os.getenv('SECRET_KEY', 'tu_clave_secreta_muy_segura_cambiala_en_produccion')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '60'))

security = HTTPBearer()

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('sub') or payload.get('email')
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token inválido')
        return email
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token inválido') from e

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    email = verify_token(credentials.credentials)
    user = db.query(Profesora).filter(Profesora.email == email).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Usuario no encontrado',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    return user

def get_current_admin(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    user = get_current_user(credentials, db)
    if not getattr(user, 'is_admin', False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Se requieren privilegios de administrador')
    return user
