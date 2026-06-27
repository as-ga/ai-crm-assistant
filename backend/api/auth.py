from fastapi import APIRouter, Depends, Response, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
import models
from database import get_db
import services.jwt as jwt
from middleware import auth_middleware

auth = APIRouter()


class RequestResponse(BaseModel):
    message: str
    data: Optional[Any] = None


class RegisterUserRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr  # Automatic email format validate karega
    password: str = Field(..., min_length=6)


class LoginUserRequest(BaseModel):
    email: EmailStr
    password: str


@auth.post("/register", response_model=RequestResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: RegisterUserRequest, db: AsyncSession = Depends(get_db)):
    # 1. Check if user already exists
    # Note: production me .scalars() use karein query standard rakhne ke liye
    query = models.User.__table__.select().where(models.User.email == user.email)
    result = await db.execute(query)
    user_existing = result.first()

    if user_existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    # 2. Save new user (TIP: Password ko yahan hash_password(user.password) zaroor karein)
    new_user = models.User(
        name=user.name,
        email=user.email,
        password=user.password  # Raw password unsafe hai, ise production me hash karein
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)  # Refresh se generated ID mil jati hai

    return {
        "message": "User registered successfully",
        "data": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        }
    }


@auth.post("/login", response_model=RequestResponse)
async def login_user(user: LoginUserRequest, response: Response, db: AsyncSession = Depends(get_db)):
    # 1. Fetch User
    query = models.User.__table__.select().where(models.User.email == user.email)
    result = await db.execute(query)
    user_exist = result.first()

    # 2. Verify credentials
    if not user_exist or user_exist.password != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # 3. Create Token
    token = jwt.create_jwt_token({
        "id": user_exist.id,
        "name": user_exist.name,
        "email": user_exist.email
    })

    # 4. Set Secure Cookie
    response.set_cookie(
        key="token",
        value=token,
        max_age=3600,  # expires ki jagah max_age seconds me best practice hai
        httponly=True,
        secure=True,    # HTTPS ke liye (Production mandatory)
        samesite="lax"  # CSRF protection ke liye
    )

    return {
        "message": "Login successful",
        "data": {
            "token": token,
            "user": {
                "id": user_exist.id,
                "name": user_exist.name,
                "email": user_exist.email
            }
        }
    }


@auth.get("/me", response_model=RequestResponse)
async def get_user_info(db: AsyncSession = Depends(get_db), current_user: dict = Depends(auth_middleware)):
    query = models.User.__table__.select().where(
        models.User.id == current_user.get("id"))
    result = await db.execute(query)
    user = result.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {
        "message": "User found",
        "data": {
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
        }
    }


@auth.post("/logout", response_model=RequestResponse)
async def logout_user(response: Response):
    response.delete_cookie(key="token", httponly=True,
                           samesite="lax", secure=True)
    return {"message": "Logged out successfully"}
