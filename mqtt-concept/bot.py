import asyncio
import random
import asyncio_mqtt as mqtt
from asyncio_mqtt import Topic

BROKER = 'broker.hivemq.com'  # MQTT broker address
PORT = 1883  # MQTT broker port
TOPIC = 'control'  # MQTT topic to listen to

temperature_data = {
    'last_average_temperature': None
}

async def check_zone_temperatures_task(client):
    while True:
        await asyncio.sleep(60)  # Wait for 60 seconds
        temperature_data['last_average_temperature'] = calculate_average_temperature()
        print(f"Calculated average temperature: {temperature_data['last_average_temperature']}")
        await publish_temperature(client, temperature_data['last_average_temperature'])

def calculate_average_temperature():
    return round(random.uniform(60, 80), 2)

def is_temperature_within_range(temperature):
    return 65 <= temperature <= 75

async def publish_temperature(client, temperature):
    await client.publish('temperature', str(temperature))

async def handle_message(client):
    topic_filter = Topic(TOPIC)
    async with client.messages() as messages:
        async for message in messages:
            if topic_filter.matches(message.topic):
                payload = message.payload.decode()
                print(f"Received message on topic {message.topic}: {payload}")
                if payload == 'check temps':
                    # Respond with the last average temperature
                    last_temperature = temperature_data['last_average_temperature']
                    print("Publishing last temperature:",last_temperature)
                    await publish_temperature(client, last_temperature)

async def main():
    async with mqtt.Client(BROKER) as client:
        await client.connect()
        await client.subscribe(TOPIC)  # Subscribe to the specified topic

        tasks = [
            check_zone_temperatures_task(client),
            publish_temperature(client, 0),  # Initial temperature publishing
            handle_message(client)
        ]

        await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
