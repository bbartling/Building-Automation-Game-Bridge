from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# We'll use global variables for this simple example
# In a real application, you might want to use a database or other persistent storage method
NUM_VAV_BOXES = 10
zone_setpoints = [70.0] * NUM_VAV_BOXES  # In degrees Fahrenheit

@app.route('/hvac_status', methods=['GET'])
def get_hvac_status():
    # Return a random HVAC status (1 for on, 0 for off)
    return jsonify({"hvac_status": random.randint(0, 1)})

@app.route('/zone_temperatures', methods=['GET'])
def get_zone_temperatures():
    # Return a list of random temperatures for each VAV box
    zone_temperatures = [random.uniform(60.0, 80.0) for _ in range(NUM_VAV_BOXES)]  # In degrees Fahrenheit
    return jsonify({"zone_temperatures": zone_temperatures})

@app.route('/zone_setpoints', methods=['GET'])
def get_zone_setpoints():
    # Return the current zone setpoints
    return jsonify({"zone_setpoints": zone_setpoints})

@app.route('/outdoor_conditions', methods=['GET'])
def get_outdoor_conditions():
    # Return random outdoor conditions (temperature and humidity)
    outdoor_conditions = {"temperature": random.uniform(60.0, 90.0), "humidity": random.uniform(20.0, 80.0)}  # Temperature in degrees Fahrenheit
    return jsonify({"outdoor_conditions": outdoor_conditions})

@app.route('/occupancy_status', methods=['GET'])
def get_occupancy_status():
    # Return a random occupancy status for each VAV box (1 for occupied, 0 for unoccupied)
    occupancy_status = [random.randint(0, 1) for _ in range(NUM_VAV_BOXES)]
    return jsonify({"occupancy_status": occupancy_status})

@app.route('/set_zone_setpoints', methods=['POST'])
def set_zone_setpoints():
    global zone_setpoints
    zone_setpoints = request.json["zone_setpoints"]
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)
