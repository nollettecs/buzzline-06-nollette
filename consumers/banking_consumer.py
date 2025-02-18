import json
import time
from collections import defaultdict, deque
import matplotlib.pyplot as plt
import numpy as np
import logging
from confluent_kafka import Consumer, KafkaException

# Configure logging
logging.basicConfig(
    filename="logs/banking_consumer.log",  # Save logs inside logs folder
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

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

# Store amounts for the line graph
max_points = 50  # Limit the number of points for clarity
timestamps = deque(maxlen=max_points)
amounts = deque(maxlen=max_points)

# Use a modern, bright style
plt.style.use('seaborn-v0_8-bright')

# Create figure and subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
plt.ion()  # Enable interactive mode

# Function to update and display the bar chart
def update_bar_chart():
    ax1.cla()  # Clear only the first subplot

    # Define colors for different transaction types
    color_map = {
        'deposit': '#1f77b4',  # Blue
        'withdraw': '#d62728',  # Red
        'low_balance': '#ff7f0e',  # Orange
        'current_balance': '#2ca02c',  # Green
        'checking_account': '#9467bd',  # Purple
        'savings_account': '#8c564b'  # Brown
    }

    # Prepare data
    transaction_types = list(transaction_counts.keys())
    counts = list(transaction_counts.values())
    colors = [color_map.get(t_type, 'gray') for t_type in transaction_types]

    # Plot the bar chart
    bars = ax1.bar(transaction_types, counts, color=colors, edgecolor='black', alpha=0.85)

    # Annotate bars with their values
    for bar in bars:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, yval + 0.2, str(yval),
                 ha='center', fontsize=10, fontweight='bold')

    # Customize the graph
    ax1.set_xlabel("Transaction Type", fontsize=12, fontweight='bold')
    ax1.set_ylabel("Count", fontsize=12, fontweight='bold')
    ax1.set_title("📊 Vibrant Transaction Type Distribution", fontsize=14, fontweight='bold')
    ax1.set_xticklabels(transaction_types, rotation=15, fontsize=10)
    ax1.grid(axis='y', linestyle='--', alpha=0.7)
    ax1.set_ylim(0, max(counts) + 2)

# Function to update and display the line chart
def update_line_chart():
    ax2.cla()  # Clear only the second subplot

    # Check if there's data to plot
    if len(timestamps) > 1:
        ax2.plot(timestamps, amounts, marker='o', linestyle='-', color='#ff5733', linewidth=2, alpha=0.85)
        ax2.set_xlabel("Transaction Count", fontsize=12, fontweight='bold')
        ax2.set_ylabel("Amount ($)", fontsize=12, fontweight='bold')
        ax2.set_title("📈 Transaction Amount Trend Over Time", fontsize=14, fontweight='bold')
        ax2.grid(True, linestyle='--', alpha=0.6)

# Function to consume messages
def consume_messages():
    try:
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
                transaction = json.loads(raw_message)

                transaction_type = transaction.get('transaction_type', 'unknown')
                amount = transaction.get('amount', 0.0)

                # Debugging: Print every received message
                print(f"Received Transaction: {transaction}")

                # Increment transaction count
                transaction_counts[transaction_type] += 1

                # Store transaction amount for the line graph
                timestamps.append(len(timestamps) + 1)  # Simple counter for x-axis
                amounts.append(amount)

                # High Alert for Low Balance Transactions
                if transaction_type == 'low_balance':
                    alert_message = f"⚠️ HIGH ALERT: Low balance detected! {transaction}"
                    print(alert_message)
                    logging.warning(alert_message)  # Also log the alert to the logs file

                # Update both visualizations
                update_bar_chart()
                update_line_chart()
                plt.pause(0.1)

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