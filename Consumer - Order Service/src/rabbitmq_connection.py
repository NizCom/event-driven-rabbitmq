import json
import logging
import pika
import time

from .mongodb_connection import save_order_in_db

ORDER_SERVICE_QUEUE = 'order_service'
ORDER_BROADCAST_EXCHANGE = 'order_broadcast'
DEAD_LETTER_QUEUE = 'dead_letter_queue'
DEAD_LETTER_EXCHANGE = 'dead_letter_exchange'
ROUTING_KEY_NEW_ORDERS = 'order.new'
RETRY_DELAY = 5
ARGUMENTS = {'x-dead-letter-exchange': 'dead_letter_exchange'}

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def connect_to_rabbitmq_and_bind_queue():
    connected = False

    while not connected:
        try:
            logging.info("Connecting to RabbitMQ...")
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            channel = connection.channel()

            declare_dead_letter_exchange(channel)
            channel.queue_declare(queue=ORDER_SERVICE_QUEUE, durable=True, arguments=ARGUMENTS)

            logging.info("Attempting to bind queue to exchange...")
            channel.queue_bind(exchange=ORDER_BROADCAST_EXCHANGE, queue=ORDER_SERVICE_QUEUE,
                               routing_key=ROUTING_KEY_NEW_ORDERS)
            connected = True

        except pika.exceptions.ChannelClosedByBroker as e:
            logging.exception(f"Exchange not found. Retrying in {RETRY_DELAY} seconds... {e}")
            time.sleep(RETRY_DELAY)
        except pika.exceptions.AMQPConnectionError as e:
            logging.exception(f"Connection error. Retrying in {RETRY_DELAY} seconds... {e}")
            time.sleep(RETRY_DELAY)
        except Exception as e:
            logging.exception(f"Unexpected error: {e}")
            time.sleep(RETRY_DELAY)

    logging.info(f"Queue '{ORDER_SERVICE_QUEUE}' successfully bound to exchange "
                 f"'{ORDER_BROADCAST_EXCHANGE}' with routing key '{ROUTING_KEY_NEW_ORDERS}'.")

    return channel


def callback(ch, method, properties, body):
    try:
        order = json.loads(body.decode('utf-8'))
        logging.info("New order received")
        process_new_order(order)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        logging.exception(f" [!] Error processing message: {e}")


def start_rabbitmq():
    channel = connect_to_rabbitmq_and_bind_queue()
    channel.basic_consume(queue=ORDER_SERVICE_QUEUE, on_message_callback=callback)
    logging.info(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


def calculate_shipping_cost(total_amount: float) -> float:
    shipping_cost = total_amount * 0.02
    return round(shipping_cost, 2)


def process_new_order(order):
    order['shippingCost'] = calculate_shipping_cost(order['totalAmount'])
    save_order_in_db(order)
    del order['_id']  # No need for '_id' field from MongoDB
    logging.info(f"Order stored with ID {order['orderId']}."
                 f" Order details: {json.dumps(order, indent=4)}")


def declare_dead_letter_exchange(channel):
    channel.exchange_declare(exchange='dead_letter_exchange', exchange_type='fanout')
    channel.queue_declare(queue=DEAD_LETTER_QUEUE, durable=True)
    channel.queue_bind(exchange=DEAD_LETTER_EXCHANGE, queue=DEAD_LETTER_QUEUE)
