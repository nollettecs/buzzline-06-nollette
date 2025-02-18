import json
import os
import logging
import random
import time
import uuid
from confluent_kafka import Producer

# Ensure the logs directory exists
log_directory = "logs"
os.makedirs(log_directory, exist_ok=True)  # Create logs directory if it doesn't exist

logging.basicConfig(
    filename=os.path.join(log_directory, "banking_producer.log"),  # Store in logs folder
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force=True  # Ensure logging is properly configured
)

# Kafka Producer Configuration
conf = {
    'bootstrap.servers': 'localhost:9092',
}

producer = Producer(conf)

# Function to validate transaction data
def validate_transaction(transaction):
    """Ensure transaction data is valid."""
    if 'amount' not in transaction or not isinstance(transaction['amount'], (float, int)):
        error_message = f"Invalid amount in transaction: {transaction}"
        print(error_message)
        logging.error(error_message)
        return False
    if 'transaction_type' not in transaction or transaction['transaction_type'] not in ['deposit', 'withdraw', 'low_balance', 'current_balance', 'checking_account', 'savings_account']:
        error_message = f"Invalid transaction type in transaction: {transaction}"
        print(error_message)
        logging.error(error_message)
        return False
    return True

# Function to produce a transaction message to Kafka
def produce_transaction(transaction):
    """Sends a validated transaction message to Kafka."""
    if validate_transaction(transaction):
        producer.produce('bank_alerts', json.dumps(transaction).encode('utf-8'))
        producer.flush()  # Ensure the message is sent
        logging.info(f"Produced transaction: {transaction}")

# Function to simulate generating random transactions
def generate_transaction():
    """Generate a random banking transaction."""
    transaction_types = ['deposit', 'withdraw', 'low_balance', 'current_balance', 'checking_account', 'savings_account']
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
    logging.info("Banking Producer started.")
    try:
        while True:
            # Generate a random transaction
            transaction = generate_transaction()
            print(f"Producing transaction: {transaction}")
            logging.info(f"Generating transaction: {transaction}")

            # Send the transaction to Kafka
            produce_transaction(transaction)
            
            # Wait before sending the next transaction
            time.sleep(3.0)  # Random delay 3 seconds
    except KeyboardInterrupt:
        print("Producer interrupted. Exiting...")
        logging.info("Banking Producer stopped.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        producer.flush()

# Run the producer
if __name__ == "__main__":
    main()

