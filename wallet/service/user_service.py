import random
from fastapi import HTTPException
from wallet.model.user_model import UserModel
from wallet.repo.user_repo import UserRepo
from wallet.utils.logger import LogSubject

class UserService:
    def __init__(self):
        self.user_repo = UserRepo()
        self._log = LogSubject()

    def register_user(self, data: UserModel):
        self._log.notify(f'Attempting to register {data.user_name}', 'INFO')
        # Generate a unique account number
        acc_num = None
        for _ in range(100):  # Try up to 100 times
            temp_num = str(random.randint(1, 10000))
            if not self.user_repo.find_user(temp_num):
                acc_num = temp_num
                break
        if not acc_num:
            self._log.notify(f'Failed to generate a unique number after 100 attempts', 'ERROR')
            raise HTTPException(500, "Could not create account number")

        # Create the user
        self.user_repo.add_user(
            acc_num=acc_num,
            name=data.user_name,
            tier=data.user_type
        )

        # Verify the user was created
        created_user = self.user_repo.find_user(acc_num)
        if not created_user:
            self._log.notify(f"Registration failed for account number: {acc_num}", "ERROR")
            raise HTTPException(400, "Registration failed")
        self._log.notify(f"Successfully registered user: {acc_num}", "INFO")
        return created_user

    def get_user(self, acc_num ):
        self._log.notify(f"Attempting to find user with account number: {acc_num}", "INFO")
        user = self.user_repo.find_user(acc_num)
        if not user:
            self._log.notify(f"User not found: {acc_num}", "WARNING")
            raise HTTPException(404, "User not found")
        self._log.notify(f"Found user: {acc_num}", "INFO")
        return user