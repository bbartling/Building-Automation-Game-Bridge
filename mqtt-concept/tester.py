import asyncio
import asyncio_mqtt as mqtt

BROKER = 'broker.hivemq.com'  # MQTT broker address
PORT = 1883                    # MQTT broker port
TOPIC = 'control'              # MQTT topic to publish to
RESPONSE_TOPIC = 'temperature' # MQTT topic to listen to for responses

async def publish_message(client):
    while True:
        message = input("Enter message to publish (or 'exit' to quit): ")
        if message == 'exit':
            break
        await client.publish(TOPIC, message)

async def subscribe_and_print(client):
    await client.subscribe(RESPONSE_TOPIC)
    async with client.unfiltered_messages() as messages:
        async for message in messages:
            print(f'Received response message on topic {message.topic}: {message.payload.decode()}')

async def main():
    async with mqtt.Client(BROKER, port=PORT) as client:
        await client.connect()
        tasks = [
            publish_message(client),
            subscribe_and_print(client)
        ]
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
