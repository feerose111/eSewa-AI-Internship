from fastapi import APIRouter, Depends
from wallet.service.user_service import UserService
from wallet.utils.depedency import get_user_service
from wallet.model.user_model import UserModel

router = APIRouter(tags=["user"], prefix="/users")

@router.get("/")
async def home():
    return {
        'message': 'Welcome to your digital wallet'
    }

@router.post("/register")
async def register_user(
    user: UserModel,
    service: UserService = Depends(get_user_service)
):
    return await service.register_user(user)

@router.post("/{acc_num}")
async def signin_user(acc_num: str,
                      service: UserService = Depends(get_user_service)):
    return await service.get_user(acc_num)

