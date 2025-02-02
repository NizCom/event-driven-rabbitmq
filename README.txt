1. Details
- Name: Nizan Naor 
- ID: 313546822


2. Endpoints
Producer:
- http://localhost:5000/create-order 
- POST
- JSON: {
	  "orderId": str,
	  "itemsNum": int
	}
	
Consumer:
- http://localhost:8080/order-details
- GET
- Query Params: "orderId"


3. I chose a direct exchange, because it ensures that only messages with the routing key 'new' are delivered to the consumer.
So there is no need to filter the messages manualy (using if statement), and it simplifies the logic and reduces unnecessary processing.


4. The binding on the consumer is 'new' to ensure it receives only messages about new orders, as this consumer handles new orders. 


5.
a) The publisher declares the exchange, because the producer must ensure the exchange exists before publishing messages to it.
If it doesn't exist, the producer won't be able to publish messages and it'll lead to failures.

b) The consumer declares the queue, because this is the resource which uses the queue for receiving messages from the producer.



** The consumer saves the new orders in MongoDB - docker-compose runs mongo image as well.