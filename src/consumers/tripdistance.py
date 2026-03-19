import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from kafka import KafkaConsumer

from models import ride_deserializer

server = "localhost:9092"
topic_name = "green-trips"

consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=[server],
    auto_offset_reset="earliest",
    group_id="rides-console",
    value_deserializer=ride_deserializer,
)

print(f"Listening to {topic_name}...")

count = 0
for msg in consumer:
    ride = msg.value
    if ride.trip_distance > 5.0:
        count += 1
        print(f"Count: {count}, Trip > 5km: {ride}")
consumer.close()

print(f"Trips > 5km: {count}")