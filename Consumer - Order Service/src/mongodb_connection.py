import time
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_mongo_client():
    client = None
    while not client:
        try:
            client = MongoClient('mongodb://mongo:27017/')
            logging.info("Connected to MongoDB")
        except ConnectionFailure:
            logging.warning("MongoDB is not ready. Retrying in 5 seconds...")
            time.sleep(5)
    return client


client = get_mongo_client()
db = client['orders_db']
orders_collection = db['orders']


def get_order_by_id(order_id):
    if not order_id:
        raise ValueError("Missing 'orderId' query parameter.")

    if not isinstance(order_id, str):
        raise TypeError(f"Expected a string, but got {type(order_id).__name__}")

    order = orders_collection.find_one({'orderId': order_id})

    if not order:
        raise ValueError(f"OrderId '{order_id}' does not exist.")

    order.pop('_id', None)

    return order


def save_order_in_db(order_to_add):
    orders_collection.delete_many({"orderId": order_to_add["orderId"]})
    orders_collection.insert_one(order_to_add)
