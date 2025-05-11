from wallet.utils.config import TIER_RULES
from wallet.repo.user_repo import UserRepo

def get_user_tier_info(user_repo: UserRepo, user_id):
    tier = user_repo.find_user(user_id , by_acc_num=False)
    return TIER_RULES.get(tier, TIER_RULES["basic"]), tier
