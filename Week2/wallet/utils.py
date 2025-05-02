TIER_RULES = {
    "basic": {
        "max_per_transaction": 5000,
        "max_daily_total": 10000,
        "transfer_fee_percent": 1.25
    },
    "premium": {
        "max_per_transaction": 500000,
        "max_daily_total": 100000,
        "transfer_fee_percent": 0.75
    },
    "business": {
        "max_per_transaction": 100000,
        "max_daily_total": 500000,
        "transfer_fee_percent": 0.5
    }
}

def get_user_tier_info(user_id):
    from db import get_user_tier
    tier = get_user_tier(user_id)
    return TIER_RULES.get(tier, TIER_RULES["basic"]), tier
