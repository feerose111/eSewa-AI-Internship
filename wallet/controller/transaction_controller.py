from fastapi import APIRouter, Depends, HTTPException
from wallet.service.transaction_service import TransactionService
from wallet.utils.depedency import get_transaction_service
from wallet.model.transaction_model import TransactionModel
from decimal import Decimal

router = APIRouter(tags=["transactions"], prefix="/transactions")

@router.get("/")
async def home():
    return {"message": "Transaction endpoints"}

@router.get("/balance/{user_id}")
async def get_balance(user_id: int):
    data = TransactionModel(
        id = user_id,
        tx_type="balance",
        amount=Decimal('0.00'),
        status="pending",
        remarks="show balance"
    )
    service = TransactionService(data)
    return {"balance": service.get_balance()}

@router.post("/deposit")
async def deposit(
    data: TransactionModel,
    service: TransactionService = Depends(get_transaction_service)
):
    if service.deposit():
        return {
            "status": "success",
            "new_balance": service.get_balance(),
            "amount_deposited": data.amount
        }
    raise HTTPException(400, "Deposit failed")

@router.post("/withdraw")
async def withdraw(
    data: TransactionModel,
    service: TransactionService = Depends(get_transaction_service)
):
    if service.withdraw():
        return {
            "status": "success",
            "new_balance": service.get_balance(),
            "amount_withdrawn": data.amount
        }
    raise HTTPException(400, "Withdrawal failed")

@router.post("/transfer")
async def transfer(
    data: TransactionModel,
    receiver_id: int,
    service: TransactionService = Depends(get_transaction_service)
):
    if service.transfer(receiver_id):
        return {
            "status": "success",
            "new_balance": service.get_balance(),
            "receiver_id": receiver_id,
            "amount_transferred": data.amount
        }
    raise HTTPException(400, "Transfer failed")