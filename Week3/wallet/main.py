from fastapi import FastAPI
from Week3.wallet.controller import user_controller
from Week3.wallet.controller import transaction_controller
app = FastAPI()

app.include_router(user_controller.router, prefix="/users")
app.include_router(transaction_controller.router, prefix="/transactions")

