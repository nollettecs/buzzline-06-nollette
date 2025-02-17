import json
import time
from collections import defaultdict
import matplotlib.pyplot as plt
from confluent_kafka import Consumer, KafkaException

# Kafka Consumer Configuration
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'banking-consumer-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['bank_alerts'])

# Transaction counter for visualization
transaction_counts = defaultdict(int)

# Function to update and display the bar chart
def update_chart():
    plt.clf()  # Clear the previous plot
    plt.bar(transaction_counts.keys(), transaction_counts.values(), color=['blue', 'red', 'orange'])
    plt.xlabel("Transaction Type")
    plt.ylabel("Count")
    plt.title("Transaction Type Distribution")
    plt.pause(0.1)  # Pause to update the plot

# Function to consume messages
def consume_messages():
    try:
        plt.ion()  # Enable interactive mode for live updates
        while True:
            msg = consumer.poll(1.0)  # Wait for messages

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaException._PARTITION_EOF:
                    continue
                else:
                    print(f"Kafka error: {msg.error()}")
                    break

            try:
                raw_message = msg.value().decode('utf-8')
                print(f"Received Raw Kafka Message: {raw_message}")  # Debugging output
                transaction = json.loads(raw_message)

                transaction_type = transaction.get('transaction_type', 'unknown')
                amount = transaction.get('amount', 0.0)

                # Increment transaction count
                transaction_counts[transaction_type] += 1

                # Alert for low balance transactions
                if transaction_type == 'low_balance':
                    print(f"⚠️ HIGH ALERT: Low balance detected! {transaction}")

                # Update the visualization
                update_chart()

            except json.JSONDecodeError:
                print(f"Error decoding JSON: {msg.value()}")  # Debugging output
                continue

    except KeyboardInterrupt:
        print("Consumer interrupted. Exiting...")
    finally:
        consumer.close()

# Run the consumer
if __name__ == "__main__":
    consume_messages()


