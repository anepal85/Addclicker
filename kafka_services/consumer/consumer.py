import sys
import os
import logging
from confluent_kafka import Consumer, KafkaError
from datetime import datetime

# Adjust the path if necessary
DIR_NAME = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if DIR_NAME not in sys.path:
    sys.path.append(DIR_NAME)

from models.models import ClickEvent, ClickCount
from db import get_session

class ClickConsumer:
    def __init__(self, config, session, log_file='consumer.log'):
        # Configure logging
        self.logger = logging.getLogger('ClickConsumer')
        self.logger.setLevel(logging.INFO)

        # Create a file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)

        # Create a console handler (optional)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Add the formatter to the handlers
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add the handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        # Configure Kafka consumer
        self.consumer = Consumer(config)
        self.session = session

    def consume(self, topics):
        self.consumer.subscribe(topics)
        self.logger.info(f"Subscribed to topics: {topics}")
        running = True
        try:
            while running:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                elif not msg.error():
                    try:
                        self.process_message(msg)
                    except Exception as e:
                        self.logger.error(f"Error processing message: {e}")
                elif msg.error().code() != KafkaError._PARTITION_EOF:
                    self.logger.error(f"Consumer error: {msg.error()}")
                    running = False
        except KeyboardInterrupt:
            self.logger.info("Consumer interrupted by user")
        finally:
            self.consumer.close()
            self.session.close()
            self.logger.info("Consumer closed")

    def process_message(self, msg):
        button_id = msg.value().decode('utf-8')
        # Record the click event
        click_event = ClickEvent(button_id=button_id)
        self.session.add(click_event)
        # Update the click count per hour
        current_hour = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
        click_count = (
            self.session.query(ClickCount)
            .filter_by(button_id=button_id, hour=current_hour)
            .first()
        )
        if click_count:
            click_count.count += 1
        else:
            click_count = ClickCount(button_id=button_id, hour=current_hour, count=1)
            self.session.add(click_count)
        self.session.commit()
        self.logger.info(f"Recorded click event for button_id: {button_id}")

def main():
    import os

    # Configure Kafka consumer
    conf = {
        'bootstrap.servers': "localhost:9092",
        'group.id': "clicks_group",
        'auto.offset.reset': 'earliest'
    }
    # Create a new session
    session = get_session()
    # Create the consumer
    click_consumer = ClickConsumer(conf, session, log_file='consumer.log')
    # Start consuming
    click_consumer.consume(['clicks_topic'])

if __name__ == '__main__':
    main()
