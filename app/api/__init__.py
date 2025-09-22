from fastapi import APIRouter

from app.api import translation
from app.api import authorization

router = APIRouter()

router.include_router(translation.router, prefix="/translation")
router.include_router(authorization.router, prefix="/authorization")