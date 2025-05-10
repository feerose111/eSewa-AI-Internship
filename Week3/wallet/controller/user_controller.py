from fastapi import APIRouter, Depends
from Week3.wallet.view.user_view import UserService
from Week3.wallet.utils.depedency import get_user_service
from Week3.wallet.model.user_model import UserModel

router = APIRouter(tags=["user"])

@router.get("/")
async def home():
    return {
        'message': 'Welcome to your digital wallet'
    }

@router.post("/register")
async def register_user(user: UserModel,
                        user_service : UserService = Depends(get_user_service)):
    return await user_service.register_user(user)

@router.post("/signin")
async def signin_user(user: UserModel,
                      user_service: UserService = Depends(get_user_service)):
    return await user_service.get_user(user)

