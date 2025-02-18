# Buzzline-06-Nollette

## Author: Cole Nollette

- **Date:** 2/17/25
- **Course:** 44-671 Module 6

---

## Overview

This project implements a Kafka-based event streaming system to simulate banking transactions. It includes:

- **Producer:** Generates and sends realistic banking alerts (e.g., deposits, withdrawals, low balance, etc. warnings) to a Kafka topic.
- **Consumer:** Listens for banking alerts, processes them, filters and sends necessary high-alert messages, and visualizes transaction trends using bar and line charts.

The system is designed to work in real-time, leveraging Kafka for message queuing and Python for data processing and visualization.

1. Transaction Type Distribution

    - Tracks and visualizes different types of banking transactions (deposits, withdrawals, low balance alerts, etc.).
    - Helps in identifying which transaction types occur most frequently.

2. Real-Time Trend of Transaction Amounts

    - A line graph shows the trend of transaction amounts over time.
    - Useful for detecting patterns, spikes, or anomalies in banking activity.

3. High-Alert Notifications (Low Balance Warnings)

    - Detects low balance transactions and raises immediate alerts.
    - Can be expanded for fraud detection or customer notifications.

4. Streaming Data Processing with Kafka

    - Demonstrates real-time data ingestion and processing.
    - Efficiently handles high-throughput banking messages.

5. Consumer-Producer Architecture

    - Simulates how banking transactions are produced and consumed in a scalable environment.
    - Lays the foundation for implementing machine learning models or anomaly detection in banking data.


---

## 1. Prerequisites

Before starting, ensure you have completed the setup tasks in:

- [Buzzline-01-Case](https://github.com/denisecase/buzzline-01-case)
- [Buzzline-02-Case](https://github.com/denisecase/buzzline-02-case)

**Requirements:**

- Python 3.11
- Kafka installed and running
- Required dependencies installed (via `requirements.txt`)

---

## 2. Setting Up the Project

### a. Clone and Set Up Virtual Environment

1. Clone this repository.
2. Navigate into the project folder.
3. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Mac/Linux
   .venv\Scripts\activate    # Windows
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 3. Starting Kafka Services

Ensure **Zookeeper** and **Kafka** are running.

### a. Start Zookeeper (Terminal 1)

```bash
bin/zookeeper-server-start.sh config/zookeeper.properties
```

``` brew services start zookeeper```

### b. Start Kafka (Terminal 2)

```bash
bin/kafka-server-start.sh config/server.properties
```

``` brew services start kafka```

---

## 4. Running the Kafka Producer

The producer generates simulated banking transactions and sends them to Kafka.

### a. Start the Producer (Terminal 3)

```bash
source .venv/bin/activate  # Activate environment
python3 -m producers.bank_producer  # Start producer
```

### Producer Functionality

- Sends randomly generated banking transactions.
- Includes transaction types: `deposit`, `withdraw`, `low_balance`, `current_balance`, `checking_account`, and `savings_account`.
- Publishes these messages to the Kafka topic `bank_alerts`.
- Sends all messages to the `banking_producer.log`

---

## 5. Running the Kafka Consumer

The consumer listens for messages, processes transactions, filters alerts, and visualizes trends.

### a. Start the Consumer (Terminal 4)

```bash
source .venv/bin/activate  # Activate environment
python3 -m consumers.bank_consumer  # Start consumer
```

### Consumer Functionality

- **Processes Transactions**
  - Listens to the Kafka topic `bank_alerts`.
  - Extracts transaction type and amount from messages.
- **Filters High-Alert Messages**
  - Detects `low_balance` transactions and logs a high-alert warning and sends this to `banking_consumer.log`.
- **Real-Time Visualization**
  - **Bar Chart:** Displays transaction type distribution with dynamic updates.
  - **Line Graph:** Tracks transaction amount trends over time.

---

## 6. Visualization Features

- **Bar Chart:** Shows the count of different transaction types.
- **Line Chart:** Plots the transaction amounts over time.
- **Logging:** Captures `low_balance` alerts in both console output and `logs.banking_consumer.log`. Also captures all messages in `logs.banking_producer.log`

---

## 7. Stopping Services

To stop services, use:

```bash
Ctrl+C  # Stop producer or consumer
bin/kafka-server-stop.sh  # Stop Kafka
bin/zookeeper-server-stop.sh  # Stop Zookeeper
```
``` brew services stop zookeeper ```
``` brew services stop kafka```

---

## 8. Managing Virtual Environment

When resuming work:

1. Navigate to project folder.
2. Reactivate the virtual environment.
3. Restart Zookeeper and Kafka services.
4. Start the producer and consumer.

To save space, delete `.venv` when not in use and recreate it later.

---

## License

This project is licensed under the MIT License. Feel free to fork, modify, and experiment.

---

## Notes

- Ensure Kafka is running before starting producer/consumer.
- Keep logs organized in `logs/`.
- Adjust transaction generation rates in `bank_producer.py` as needed.

This README provides a detailed guide to understanding and running the banking transaction Kafka pipeline. 🚀

