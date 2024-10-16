from flask import Flask, request, render_template

app = Flask(__name__)

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
    print("Received device control data:", data)  # Print the raw JSON data received from the device control
    return '', 204  # No content

if __name__ == '__main__':
    app.run()
