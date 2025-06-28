from passlib.context import CryptContext
from fastapi import HTTPException,Depends
from datetime import datetime, timedelta
from fastapi.security import *
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from database import get_db
import models

SECRET_KEY = "secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

# oauth2_scheme = HTTPBasicCredentials(type="bearer")
admin_http_bearer = HTTPBearer(scheme_name="Admin Token")
http_bearer = HTTPBearer(scheme_name="Token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)




# Auth helpers



def get_current_user(credentials: HTTPAuthorizationCredentials  = Depends(http_bearer), db: Session = Depends(get_db)):
    token=credentials.credentials

    credentials_exception = HTTPException(status_code=401, detail="Invalid token")
    try:
        payload = jwt.decode(token, "secret-key", algorithms=["HS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).get(int(user_id))
    if user is None:
        raise credentials_exception
    return user


def admin_required(current_user: models.User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")
    return current_user
