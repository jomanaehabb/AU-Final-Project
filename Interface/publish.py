import paho.mqtt.client as mqtt

# Callback when a message is received
def on_message(client, userdata, message):
    print(f"Received message '{message.payload.decode()}' on topic '{message.topic}'")

# Initialize MQTT Client
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message

# Connect to the MQTT broker
mqttBroker = "mqtt.eclipseprojects.io"
mqtt_client.connect(mqttBroker)

# Subscribe to the topic
topic = "robot/control"
mqtt_client.subscribe(topic)

# Start the loop
mqtt_client.loop_start()

try:
    while True:
        pass  # Keep the script running
except KeyboardInterrupt:
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
