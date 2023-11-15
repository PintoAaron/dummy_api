from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models import User 
from utils import verify_password
from oauth2 import create_access_token



router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(request: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect password")
    
    access_token = create_access_token(data={"user_id": user.user_id, "email": user.email})
        
    return {"access_token": access_token, "token_type": "bearer"}