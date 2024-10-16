from flask import Flask, render_template_string, request
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)

# AWS IoT configuration
AWS_IOT_ENDPOINT = "your-iot-endpoint"  # Replace with your AWS IoT endpoint
AWS_IOT_PORT = 8883
AWS_IOT_TOPIC_AIRPUMP = "device/DB_testbench/airpump"
AWS_IOT_TOPIC_LINEAR_ACTUATOR = "device/DB_testbench/linearactuator"
AWS_IOT_TOPIC_MOTOR = "device/DB_testbench/motor"

# MQTT Client setup
client = mqtt.Client()
client.tls_set(ca_certs="path/to/AmazonRootCA1.pem", certfile="path/to/certificate.pem.crt", keyfile="path/to/private.pem.key")
client.connect(AWS_IOT_ENDPOINT, AWS_IOT_PORT, keepalive=60)
client.loop_start()

# HTML template with buttons
HTML_TEMPLATE = '''
<!doctype html>
<html>
<head>
    <title>Control Interface</title>
</head>
<body>
    <h1>Device Control</h1>
    <h2>Motors</h2>
    <button onclick="sendCommand('motor', 'active', '1')">Motor 1 On</button>
    <button onclick="sendCommand('motor', 'active', '0')">Motor 1 Off</button>
    <button onclick="sendCommand('motor', 'curing', '1')">Motor 2 On</button>
    <button onclick="sendCommand('motor', 'curing', '0')">Motor 2 Off</button>
    
    <h2>Air Pumps</h2>
    <button onclick="sendCommand('airpump', 'curing', '1', '1')">Airpump 1 On</button>
    <button onclick="sendCommand('airpump', 'curing', '1', '0')">Airpump 1 Off</button>
    <button onclick="sendCommand('airpump', 'curing', '2', '1')">Airpump 2 On</button>
    <button onclick="sendCommand('airpump', 'curing', '2', '0')">Airpump 2 Off</button>
    
    <h2>Linear Actuator</h2>
    <button onclick="sendCommand('linearactuator', '1', '0', 'extend')">Linear Actuator Extend</button>
    <button onclick="sendCommand('linearactuator', '1', '0', 'retract')">Linear Actuator Retract</button>
    
    <script>
        function sendCommand(device, phase, active, compartment) {
            fetch('/send', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ device: device, phase: phase, active: active, compartment: compartment }),
            });
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

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
            "side": "0",
            "action": active  # 'extend' or 'retract'
        }
        client.publish(AWS_IOT_TOPIC_LINEAR_ACTUATOR, json.dumps(message))

    elif device == 'motor':
        message = {
            "phase": phase,
            "active": active
        }
        client.publish(AWS_IOT_TOPIC_MOTOR, json.dumps(message))

    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
