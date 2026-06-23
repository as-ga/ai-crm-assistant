from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
import models
from database import get_db

auth = APIRouter()


class UserRegistrationRequest(BaseModel):
    name: str
    email: str
    password: str


class UserRegistrationResponse(BaseModel):
    message: str


@auth.post("/register", response_model=UserRegistrationResponse)
async def register_user(user: UserRegistrationRequest, db: AsyncSession = Depends(get_db)):
    try:
        user_existing = await db.execute(
            models.User.__table__.select().where(models.User.email == user.email)
        )
        user_existing = user_existing.scalar_one_or_none()
        if user_existing:
            return {"message": "User already exists"}

        new_user = models.User(
            name=user.name, email=user.email, password=user.password)
        db.add(new_user)
        await db.commit()
        return {"message": "User registered successfully"}
    except Exception as e:
        await db.rollback()
        return {"message": f"Error registering user: {str(e)}"}
