from flask import Flask, render_template, request, jsonify
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)
# AWS IoT configuration
AWS_IOT_ENDPOINT = "a1m66o686tiqe2-ats.iot.ap-southeast-2.amazonaws.com"  # Replace with your AWS IoT endpoint
AWS_IOT_PORT = 8883
AWS_IOT_TOPIC_AIRPUMP = "device/DB_testbench/airpump"
AWS_IOT_TOPIC_LINEAR_ACTUATOR = "device/DB_testbench/linearactuator"
AWS_IOT_TOPIC_MOTOR = "device/DB_testbench/motor"

# MQTT Client setup
client = mqtt.Client()
client.tls_set(ca_certs="AmazonRootCA1.pem", certfile="DB-Comp-certificate.pem.crt", keyfile="DB-Comp-private.pem.key")
client.connect(AWS_IOT_ENDPOINT, AWS_IOT_PORT, keepalive=60)
client.loop_start()

@app.route('/')
def index():
    return render_template('final.html')  # Serves the HTML file

@app.route('/slider', methods=['POST'])
def slider():
    data = request.json
    print("Received slider data:", data)  # Print the raw JSON data received from the slider
    return '', 204  # No content

@app.route('/send', methods=['POST'])
def send():
    data = request.json
    device = data.get('device')
    phase = data.get('phase')
    active = data.get('active')
    compartment = data.get('compartment')

    if device == 'airpump':
        message = {
            "phase": phase,
            "compartment": compartment,
            "active": active
        }
        client.publish(AWS_IOT_TOPIC_AIRPUMP, json.dumps(message))

    elif device == 'linearactuator':
        message = {
            "compartment": compartment,
            "action": active  # 'extend' or 'retract'
        }
        client.publish(AWS_IOT_TOPIC_LINEAR_ACTUATOR, json.dumps(message))

    elif device == 'motor':
        message = {
            "phase": phase,
            "action": active
        }
        client.publish(AWS_IOT_TOPIC_MOTOR, json.dumps(message))
    return '', 204  # No content

if __name__ == '__main__':
    app.run()
