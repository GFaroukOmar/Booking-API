from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models, schemas, auth
from fastapi.security import  HTTPBearer

from database import get_db
router = APIRouter(prefix="/users", tags=["Users"])

# Register
@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = models.User(
        username=user.username,
        email=user.email,
        password=auth.hash_password(user.password),
        is_admin=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Login
class LoginForm(BaseModel):
    username: str
    email: str
    password: str
@router.post("/login")
def login(form_data:LoginForm , db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth.create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
# Admin: get all users
@router.get("/", response_model=list[schemas.UserOut])
def list_users(db: Session = Depends(get_db), _: models.User = Depends(auth.admin_required)):
    return db.query(models.User).all()

# Admin: delete user
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), _: models.User = Depends(auth.admin_required)):
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}
