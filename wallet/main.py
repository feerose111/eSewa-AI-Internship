from fastapi import FastAPI
from wallet.controller import user_controller
from wallet.controller import transaction_controller

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Wallet API is running"}


app.include_router(user_controller.router)
app.include_router(transaction_controller.router)

