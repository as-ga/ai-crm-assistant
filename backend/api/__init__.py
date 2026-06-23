from fastapi import APIRouter
from api.auth import auth

router = APIRouter()


router.include_router(auth, prefix="/auth", tags=["Authentication"])
