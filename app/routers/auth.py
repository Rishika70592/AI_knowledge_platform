from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from app.db.db import AsyncSessionLocal
from app.models import User
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter()

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/auth/register")
async def register(request: RegisterRequest):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.email == request.email))
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        new_user = User(
            email=request.email,
            hashed_password=hash_password(request.password),
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return {"id": str(new_user.id), "email": new_user.email}

@router.post("/auth/login")
async def login(request: LoginRequest):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.email == request.email))
        user = result.scalar_one_or_none()

        if not user or not verify_password(request.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        token = create_access_token({"sub": str(user.id), "email": user.email})
        return {"access_token": token, "token_type": "bearer"}