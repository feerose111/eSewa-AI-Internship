from Week3.wallet.utils.config import TIER_RULES
from Week3.wallet.repo.user_repo import UserRepo

def get_user_tier_info(user_id):
    tier = UserRepo.get_user_tier(user_id)
    return TIER_RULES.get(tier, TIER_RULES["basic"]), tier
