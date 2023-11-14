from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from database import get_db
from models import User
from schema import UserCreate, UserOut
from utils import get_password_hash


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Dict[str, UserOut])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        user.password = get_password_hash(user.password)
        new_user = User(name=user.name, email=user.email,
                        hashed_password=user.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"data": new_user}
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")


@router.get("/", status_code=status.HTTP_200_OK, response_model=Dict[str, List[UserOut]])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {"data": users}


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=Dict[str, UserOut])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"data": user}




@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()