from wallet.utils.db import db
from wallet.service.user_service import UserService
from wallet.service.transaction_service import TransactionService
from wallet.model.transaction_model import TransactionModel

def get_db_cursor():
    with db.get_cursor() as cursor:
        yield cursor

def get_user_service():
    return UserService()

def get_transaction_service(
    data: TransactionModel,
):
    return TransactionService(data)