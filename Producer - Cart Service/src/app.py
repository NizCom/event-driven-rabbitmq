from flask import Flask, request, jsonify
import json
import logging
from pydantic import BaseModel, ValidationError, Field
from .rabbitmq_connection import publish_order
from .order import Order

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class OrderRequestModel(BaseModel):
    orderId: str
    itemsNum: int = Field(..., ge=1, description="Number of items must be at least 1")


@app.route('/create-order', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        validated_data = OrderRequestModel(**data)
        new_order = Order(validated_data.orderId, validated_data.itemsNum)
        order_json = json.dumps(new_order.to_dict(), indent=4)
        publish_order(order_json, new_order.status)
        logging.info(f" [x] Sent order! status '{new_order.status}'")

        return jsonify({
            "message": "Order created successfully",
            "data": validated_data.dict()
        }), 200

    except ValidationError as e:
        error_details = e.errors()
        msg = error_details[0]["msg"]
        error_message = {
                "error": "Validation Error",
                "message": msg
            }

        if "unable to parse string as an integer" in msg:
            error_message["required_structure"] = {
                "orderId": "str",
                "itemsNum": "int"
            }

        return jsonify(error_message), 400

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
