#scrip waits for the user to write a colour on the terminal and returns the RGB value as a json using the webcolors module
from paho.mqtt import client as mqtt_client
import webcolors
import random
import json
import sys

broker = "IP"
port = 1883 # 1883 default

# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}'
username = "User"
password = "Password"

#ask for the colour in the terminal
def get_rgb(color_name):
    while True:
        try:
            rgb = webcolors.name_to_rgb(color_name)
            rgb_to_json(rgb)
            break
        except ValueError:
            print("Invalid color name. Please try again.")
            break

def rgb_to_json(rgb):
    rgb_json = json.dumps({"r": rgb[0], "g": rgb[1], "b": rgb[2]})
    print(rgb_json)
    upload(rgb_json, "Light")

#upload the json to the MQTT broker
def upload(message, topic):
    print(f"Connecting to MQTT Broker {broker}")
    client = connect_mqtt()
    print(f"Starting loop")
    client.loop_start()
    print(f"Publishing to topic `{topic}`")
    result = client.publish(topic, message)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{message}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")
    client.loop_stop()

#connect to the MQTT broker
def connect_mqtt():
    print("connect_mqtt")
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(":(")
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

#main loop until exit is typed
if __name__ == "__main__":
    while True:
        color_name = input("Enter a color name: ")
        if color_name == "exit":
            sys.exit()
        get_rgb(color_name)
