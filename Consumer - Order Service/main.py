import threading
from src.app import app
from src.rabbitmq_connection import start_rabbitmq

if __name__ == '__main__':
    # Start the rabbitmq consumer in a separate thread
    consumer_thread = threading.Thread(target=start_rabbitmq, daemon=True)
    consumer_thread.start()

    # Run the Flask app
    app.run(host='0.0.0.0', port=8080)


