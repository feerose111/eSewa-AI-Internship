import random
from fastapi import HTTPException
from Week3.wallet.model.user_model import UserModel
from Week3.wallet.repo.user_repo import UserRepo

class UserService:

    def __init__(self):
        self.user_repo = UserRepo()

    def register_user(self,data : UserModel):
        while True:
            acc_num = random.randint(1, 10000)
            if not self.user_repo.find_user(acc_num):
                break

        self.user_repo.add_user(
            acc_num=acc_num,
            name=data.user_name,
            tier=data.user_type
        )

        valid_user = self.user_repo.find_user(acc_num)
        if not valid_user:
            raise HTTPException(status_code=400, detail="Registration failed")

        return valid_user

    async def get_user(self, data: UserModel):
        user = await self.user_repo.find_user(data.acc_num)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user