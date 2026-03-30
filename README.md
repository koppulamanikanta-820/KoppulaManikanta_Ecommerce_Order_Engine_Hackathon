# Ecommerce Order Engine

## Overview

The **Ecommerce Order Engine** is a Python-based system developed for a hackathon to simulate the processing of ecommerce orders.
It demonstrates how orders can be created, queued, processed, and tracked using multithreading and order status management.

The project focuses on building a simple order processing engine that mimics real-world ecommerce platforms where multiple orders are processed concurrently.

---

## Features

* Order creation and management
* Order status tracking (Pending, Processing, Completed, Failed)
* Multithreading for concurrent order processing
* Timestamp logging for orders
* Randomized processing time to simulate real scenarios
* Scalable structure for future improvements

---

## Technologies Used

* **Python**
* **Threading**
* **Enum**
* **Datetime**
* **Random Module**

---

## Project Structure

```
Ecommerce_Order_Engine/
│
├── main.py          # Main program to run the order engine
├── README.md        # Project documentation
```

---

## How It Works

1. Orders are generated with unique order IDs.
2. Each order starts with a **Pending** status.
3. The system processes orders using **threads**.
4. Order status changes from:

   * Pending → Processing → Completed
5. Processing time is simulated using random delays.

---

## Installation

1. Clone the repository:

```
git clone https://github.com/your-username/Ecommerce_Order_Engine.git
```

2. Navigate to the project folder:

```
cd Ecommerce_Order_Engine
```

3. Run the program:

```
python main.py
```

---

## Example Output

```
Order 1 created
Processing order 1
Order 1 completed

Order 2 created
Processing order 2
Order 2 completed
```

---

## Future Improvements

* Add database support (MySQL / PostgreSQL)
* Implement message queues (RabbitMQ / Kafka)
* Add REST API support using Flask or FastAPI
* Add logging and monitoring
* Build a frontend dashboard

---

## Author

**Manikanta Koppula**

---

## License

This project is developed for educational and hackathon purposes.
