DB_CONFIG = {
    'host' : 'localhost',
    'port' : 5432,
    'database' : 'wallet',
    'user'  : 'postgres',
    'password' : 'admin@123'

}
DATABASE_URL = "postgresql://postgres:admin@123@localhost/wallet"
# User tier rules
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