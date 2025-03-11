from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List  
from backend.database import get_db
from backend.models import User
from backend.schemas import UserResponse

router = APIRouter()

@router.get("/users", response_model=List[UserResponse])  # Используем List для списка пользователей
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    
    if not users:
        raise HTTPException(status_code=404, detail="Пользователи не найдены")
    
    return users
