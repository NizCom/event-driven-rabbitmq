import logging

from flask import Flask, request, jsonify
from .rabbitmq_connection import start_rabbitmq
from .mongodb_connection import get_order_by_id
import threading


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route('/order-details', methods=['GET'])
def get_order_details():
    try:
        order_id = request.args.get('orderId')
        order = get_order_by_id(order_id)

        return jsonify({
            "order details": order
        }), 200

    except (KeyError, TypeError) as e:
        return jsonify({
            "error": "Validation Error",
            "message": str(e)
        }), 400

    except ValueError as e:
        return jsonify({
            "error": "Order Error",
            "message": str(e)
        }), 404

    except Exception as e:
        return jsonify({
            "error": "Internal Server Error",
            "message": str(e)
        }), 500


def start_consumer_thread():
    consumer_thread = threading.Thread(target=start_rabbitmq, daemon=True)
    consumer_thread.start()


start_consumer_thread()
