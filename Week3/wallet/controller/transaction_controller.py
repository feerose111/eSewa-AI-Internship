print('transaction loaded')
from fastapi import APIRouter, Depends
from Week3.wallet.view.transaction_view import TransactionService
from Week3.wallet.utils.depedency import get_transaction_service
from Week3.wallet.model.transaction_model import TransactionModel

router = APIRouter(tags=["transactions"])

@router.get("/")
async def home():
    return {
        'message': 'transaction'
    }


@router.get("/show_balance")
async def get_balance(wallet_service : TransactionService = Depends(get_transaction_service)):
    return wallet_service.get_balance()

__all__ = ["router"]