from flask import Flask, render_template, jsonify, request
import socket
import eventlet
import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "vXjYlZ0AY3jkRGXxEFHu!"

last_response = None
last_zone_temp_response = None

available_commands = {
    "check ahu": "check_ahu",
    "check zones": "check_zone_temperatures_command",
    "check chiller plant": "check_chiller_plant",
    "check boiler plant": "check_boiler_plant",
    "check power": "check_building_power",
    "check energy": "check_energy_consumption",
    "check overrides": "check_overrides",
    "check all": "check_all",
    "check faults": "check_faults",
}

HOST = 'localhost'  # Server IP address
PORT = 12345        # Server port


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get", methods=["POST"])
def chat_interface():
    try:
        data = request.get_json()
        msg = data.get("msg")
        print("MSG: ", msg)
        if not msg:
            return jsonify({"message": "No message provided."})

        command = msg.lower()

        if command in available_commands:
            socket_event = available_commands[command]
            print("EMIT: ", socket_event)

            if msg == "check zones":
                send_message(socket_event)
                return jsonify({"message": "Waiting for response..."})

            return jsonify({"message": f"no data for {command}"})

        return jsonify({"message": "Command not recognized."})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"message": f"A server error occurred - {e}"})


def send_message(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        client_socket.sendall(message.encode())

        response = client_socket.recv(1024).decode()
        print('Received from client:', response)
        handle_zone_temperatures_response(response)


def handle_zone_temperatures_response(response):
    global last_zone_temp_response
    last_zone_temp_response = response  # Update the last response
    print("Received zone temperatures check response from client:", response)
    # Prepare the response to be sent back to the front end
    response_data = {"message": f"{response}."}
    # Perform any necessary processing with the response data
    # ...
    # Emit the response to the front end using a suitable method of your choice

'''
@app.route("/response", methods=["POST"])
def update_response():
    global last_zone_temp_response, last_response_timestamp
    data = request.get_json()
    response = data.get("response")
    timestamp = data.get("timestamp")

    if response is not None and timestamp is not None:
        if last_response_timestamp is None or timestamp > last_response_timestamp:
            last_zone_temp_response = response
            last_response_timestamp = timestamp

    return jsonify({"message": "Response received."})
'''



def background_task():
    while True:
        eventlet.sleep(60)
        send_message("check_zone_temperatures")


if __name__ == "__main__":
    eventlet.spawn(background_task)
    app.run(host="0.0.0.0", port=5000)
