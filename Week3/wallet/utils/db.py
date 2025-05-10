import psycopg2
from Week3.wallet.utils.config import DB_CONFIG


def get_connection():
    return psycopg2.connect(**DB_CONFIG)
