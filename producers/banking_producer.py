import json
from confluent_kafka import Producer
import random
import time
import uuid

# Kafka Producer Configuration
conf = {
    'bootstrap.servers': 'localhost:9092',
}

producer = Producer(conf)

# Function to validate transaction data
def validate_transaction(transaction):
    """Ensure transaction data is valid."""
    if 'amount' not in transaction or not isinstance(transaction['amount'], (float, int)):
        print(f"Error: Invalid amount in transaction: {transaction}")
        return False
    if 'transaction_type' not in transaction or transaction['transaction_type'] not in ['deposit', 'withdraw', 'low_balance']:
        print(f"Error: Invalid transaction type in transaction: {transaction}")
        return False
    return True

# Function to produce a transaction message to Kafka
def produce_transaction(transaction):
    """Sends a validated transaction message to Kafka."""
    if validate_transaction(transaction):
        producer.produce('bank_alerts', json.dumps(transaction).encode('utf-8'))
        producer.flush()  # Ensure the message is sent

# Function to simulate generating random transactions
def generate_transaction():
    """Generate a random banking transaction."""
    transaction_types = ['deposit', 'withdraw', 'low_balance']
    transaction_type = random.choice(transaction_types)
    amount = round(random.uniform(10.0, 1000.0), 2)  # Generate a random amount between 10 and 1000
    
    # Simulating a low balance alert with a specific threshold
    if transaction_type == 'low_balance':
        amount = round(random.uniform(0.0, 100.0), 2)  # Low balance alerts are usually small amounts
    
    transaction = {
        'account_id': str(uuid.uuid4()),  # Unique account ID
        'transaction_type': transaction_type,
        'amount': amount
    }
    
    return transaction

# Main loop to simulate transactions being sent to Kafka
def main():
    try:
        while True:
            # Generate a random transaction
            transaction = generate_transaction()
            print(f"Producing transaction: {transaction}")
            
            # Send the transaction to Kafka
            produce_transaction(transaction)
            
            # Wait before sending the next transaction
            time.sleep(4.0)  # Random delay 4 second
    except KeyboardInterrupt:
        print("Producer interrupted. Exiting...")

# Run the producer
if __name__ == "__main__":
    main()

