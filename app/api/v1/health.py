# health route

from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])

@router.head("/")
def health():
    """always returns 200 if running"""
    return {"status": "ok"}