from Week3.wallet.view.user_view import UserService
from Week3.wallet.view.transaction_view  import TransactionService
from Week3.wallet.model.transaction_model import TransactionModel

def get_user_service():
    return UserService()

def get_transaction_service(data: TransactionModel):
    return TransactionService(data)
