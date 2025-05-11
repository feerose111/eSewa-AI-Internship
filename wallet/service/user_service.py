import random
from fastapi import HTTPException
from wallet.model.user_model import UserModel
from wallet.repo.user_repo import UserRepo


class UserService:
    def __init__(self):
        self.user_repo = UserRepo()

    def register_user(self, data: UserModel):
        # Generate a unique account number
        account_number = None
        for _ in range(100):  # Try up to 100 times
            temp_num = str(random.randint(1, 10000))
            if not self.user_repo.find_user(temp_num):
                account_number = temp_num
                break

        if not account_number:
            raise HTTPException(500, "Could not create account number")

        # Create the user
        self.user_repo.add_user(
            acc_num=account_number,
            name=data.user_name,
            tier=data.user_type
        )

        # Verify the user was created
        created_user = self.user_repo.find_user(account_number)
        if not created_user:
            raise HTTPException(400, "Registration failed")

        return created_user

    def get_user(self, acc_num ):
        user = self.user_repo.find_user(acc_num)
        if not user:
            raise HTTPException(404, "User not found")
        return user