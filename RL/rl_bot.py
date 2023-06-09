import requests
import time, datetime, random, math

# Define the Flask server URL
FLASK_SERVER_URL = "http://localhost:5000"

def get_hvac_status():
    response = requests.get(f"{FLASK_SERVER_URL}/hvac_status")
    return response.json()["hvac_status"]

def get_zone_temperatures():
    response = requests.get(f"{FLASK_SERVER_URL}/zone_temperatures")
    return response.json()["zone_temperatures"]

def get_zone_setpoints():
    response = requests.get(f"{FLASK_SERVER_URL}/zone_setpoints")
    return response.json()["zone_setpoints"]

def get_outdoor_conditions():
    response = requests.get(f"{FLASK_SERVER_URL}/outdoor_conditions")
    return response.json()["outdoor_conditions"]

def get_occupancy_status():
    response = requests.get(f"{FLASK_SERVER_URL}/occupancy_status")
    return response.json()["occupancy_status"]

# Define the number of VAV boxes in the system
NUM_VAV_BOXES = 10

# Define the Q-learning parameters
ALPHA = 0.1  # Learning rate
GAMMA = 0.9  # Discount factor
EPSILON = 0.1  # Exploration rate

# Define the initial exploration rate and the decay rate
EPSILON_INITIAL = 1.0
EPSILON_DECAY = 0.01

# Keep track of the total number of steps taken
total_steps = 0

# Define the temperature deadband for occupant comfort
TEMP_DEADBAND = 1  # in degrees Celsius

# Initialize the Q-table
q_table = {}

# Define the continuous load management setpoint in kW
LOAD_MANAGEMENT_SETPOINT = 500

def get_time():
    # This function returns the current time of day and day of the week
    now = datetime.datetime.now()
    return now.hour, now.weekday()  # Hour: 0-23, Weekday: 0 (Monday) - 6 (Sunday)

def get_state():
    # Get the status of the HVAC system
    hvac_status = get_hvac_status()
    # Get the current temperatures in each zone
    zone_temperatures = get_zone_temperatures()
    # Get the current setpoints
    zone_setpoints = get_zone_setpoints()
    # Get the current time
    time = get_time()
    # Get the outdoor conditions
    outdoor_conditions = get_outdoor_conditions()
    # Get the occupancy status
    occupancy_status = get_occupancy_status()
    # Combine all the state information into a tuple
    state = (hvac_status,) + tuple(zone_temperatures) + tuple(zone_setpoints) + tuple(time) + tuple(outdoor_conditions) + tuple(occupancy_status)
    return state

def get_possible_actions():
    # Return the possible actions (e.g., adjusting zone setpoints) as a list
    return [2.0, 1.5, 1.0, -1.0, -1.5, -2.0]  # Adjustments in 0.5-degree increments

def get_q_value(state, action):
    # Return the Q-value for the given state-action pair from the Q-table
    if state not in q_table:
        q_table[state] = {}
    if action not in q_table[state]:
        q_table[state][action] = 0
    return q_table[state][action]

def update_q_value(state, action, new_q_value):
    # Update the Q-value in the Q-table for the given state-action pair
    q_table[state][action] = new_q_value

def choose_action(state):
    # Choose an action based on the exploration-exploitation trade-off
    if random.uniform(0, 1) < EPSILON:
        return random.choice(get_possible_actions())
    else:
        q_values = [get_q_value(state, action) for action in get_possible_actions()]
        max_q_value = max(q_values)
        best_actions = [action for action, q_value in zip(get_possible_actions(), q_values) if q_value == max_q_value]
        return random.choice(best_actions)

def perform_action(action):
    # Update the zone setpoints based on the chosen action
    zone_setpoints = get_zone_setpoints()
    for i in range(NUM_VAV_BOXES):
        zone_setpoints[i] += action
        zone_setpoints[i] = max(18.0, min(30.0, zone_setpoints[i]))  # Limiting setpoints to 18.0-30.0 range

    # Send the new setpoints to the Flask server
    requests.post(f"{FLASK_SERVER_URL}/set_zone_setpoints", json={"zone_setpoints": zone_setpoints})

    # Wait for the changes to take effect
    time.sleep(60)

def calculate_reward():
    # Code for calculating the reward

def train():
    step = 0

    while True:
        state = get_state()
        action = choose_action(state)

        perform_action(action)
        time.sleep(60)  # Wait for 60 seconds before proceeding to the next step

        new_state = get_state()
        reward = calculate_reward()

        q_value = get_q_value(state, action)
        max_next_q_value = max([get_q_value(new_state, a) for a in get_possible_actions()])
        new_q_value = q_value + ALPHA * (reward + GAMMA * max_next_q_value - q_value)

        update_q_value(state, action, new_q_value)

        print("Step:", step, "Reward:", reward)

        step += 1

        # Save the Q-values every 1000 steps
        if step % 1000 == 0:
            save_q_values()

# Run the training
train()
