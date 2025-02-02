# Order Service with RabbitMQ (Producer and Consumer)

This project demonstrates an **event-driven architecture** using **RabbitMQ** as a message broker in an order service.

### Components:
- **Producer (Order Creation)**: Sends a message to RabbitMQ with order details when a new order is created.
- **Consumer (Order Details)**: Listens to the RabbitMQ queue for new orders and stores the received data in MongoDB.

### Project Setup with Docker Compose
This project uses Docker Compose to simplify the setup and execution of all components (RabbitMQ, MongoDB, Producer, and Consumer).

### Technologies Used
- RabbitMQ for message brokering and topic exchange.
- Flask for the producer and consumer REST APIs.
- MongoDB for storing the processed order details.
- Python for both producer and consumer implementations.
- Docker Compose for running all components in isolated containers.  

### Installation and Setup
#### **1. Clone the Repository**
Clone this repository to your local machine:
```bash
git clone https://github.com/your-username/repository-name.git
cd repository-name
```  

#### **2. Set Up Docker Compose**
**1. Ensure Docker and Docker Compose are installed** on your local machine.
- Follow the installation guides for Docker and Docker Compose.
  
2. **Run Docker Compose** to start all services (RabbitMQ, MongoDB, Producer, Consumer):
```bash
docker-compose up --build
```

This will:

- Start RabbitMQ on port `5672` and management interface on `15672` (default RabbitMQ ports).
- Start MongoDB on port `27017` (default MongoDB port).
- Start the Producer (Flask API) on port `5000`.
- Start the Consumer (Flask API) on port `8080`.

#### **3. Application Endpoints**
**Producer (Order Creation)**
- Endpoint: `POST http://localhost:5000/create-order`
- Request Body (JSON):
```bash
{
  "orderId": "string",
  "itemsNum": 3
}
```
When an order is created, the producer sends a message containing the `orderId` to RabbitMQ.

**Consumer (Order Details)**
- Endpoint: GET `http://localhost:8080/order-details`
- Query Params: `orderId` (e.g., `http://localhost:8080/order-details?orderId=12345`) <br>
The consumer receives the new order message from RabbitMQ, processes it, and stores the order details in MongoDB.
