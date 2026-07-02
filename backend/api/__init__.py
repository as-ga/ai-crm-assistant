from fastapi import APIRouter
from api.auth import auth
from api.customers import customer

router = APIRouter()


router.include_router(auth, prefix="/auth", tags=["Authentication"])
router.include_router(customer, prefix="/customers", tags=["Customers"])
