from fastapi import APIRouter, Depends

from app.services.security import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/me")
def read_users_me(
    current_user: dict = Depends(get_current_user)
):
    return{
        "message": "You are authenticated",
        "user": current_user
    }
