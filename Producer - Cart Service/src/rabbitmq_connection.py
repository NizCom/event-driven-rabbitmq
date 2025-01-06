import time
import pika
import logging

ORDER_BROADCAST_EXCHANGE = 'order_broadcast'
ROUTING_KEY_ORDER = 'order'
RETRY_DELAY = 5

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def connect_to_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            return connection
        except pika.exceptions.AMQPConnectionError:
            logging.info("RabbitMQ is not ready. Retrying in 5 seconds...")
            time.sleep(RETRY_DELAY)


def publish_order(order_json, order_status):
    routing_key = f"{ROUTING_KEY_ORDER}.{order_status}"

    channel.basic_publish(
        exchange=ORDER_BROADCAST_EXCHANGE,
        routing_key=routing_key,
        body=order_json
    )


connection = connect_to_rabbitmq()
channel = connection.channel()
channel.exchange_declare(exchange=ORDER_BROADCAST_EXCHANGE, exchange_type='topic')

