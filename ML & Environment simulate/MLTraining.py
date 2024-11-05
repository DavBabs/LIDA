import numpy as np
import random
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
from lidaEnvironment import CompostingEnv

# Define the DQN model
class DQN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, output_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

# Flatten the nested state into a single list of sensor values
def flatten_state(state):
    flat_state = []
    for chamber_key in ["active_chamber", "curing_chamber"]:
        chamber_data = state[chamber_key]
        for sensor_key, values in chamber_data.items():
            if isinstance(values, np.ndarray):
                flat_state.extend(values.tolist())
            else:
                flat_state.append(float(values))
    return flat_state

# Encode and decode action for storage compatibility
def encode_action(action):
    active_chamber_action = action['active_chamber']
    curing_chamber_action = action['curing_chamber']
    return (
        (active_chamber_action['paddle'][0], active_chamber_action['paddle'][1],
         active_chamber_action['air_pump'], active_chamber_action['lid'], active_chamber_action['duration']),
        (curing_chamber_action['paddle'][0], curing_chamber_action['paddle'][1],
         curing_chamber_action['air_pump'], curing_chamber_action['lid'], curing_chamber_action['duration'])
    )

def decode_action(encoded_action):
    return {
        "active_chamber": {
            "paddle": (encoded_action[0][0], encoded_action[0][1]),
            "air_pump": encoded_action[0][2],
            "lid": encoded_action[0][3],
            "duration": encoded_action[0][4]
        },
        "curing_chamber": {
            "paddle": (encoded_action[1][0], encoded_action[1][1]),
            "air_pump": encoded_action[1][2],
            "lid": encoded_action[1][3],
            "duration": encoded_action[1][4]
        }
    }

# Define RL parameters
GAMMA = 0.99
BATCH_SIZE = 32
REPLAY_BUFFER_SIZE = 10000
EPSILON_START = 1.0
EPSILON_END = 0.1
EPSILON_DECAY = 0.995
LEARNING_RATE = 0.001
TARGET_UPDATE_FREQUENCY = 10

# Initialize environment and determine state_dim from a flattened state sample
env = CompostingEnv()
sample_state = flatten_state(env.reset())  # Flattened sample state
state_dim = len(sample_state)  # Get the length of the flattened state
action_dim = 4  # Example with 4 possible actions; adjust as needed

# Initialize DQN and optimizer with the correct input dimension
policy_net = DQN(input_dim=state_dim, output_dim=action_dim)
target_net = DQN(input_dim=state_dim, output_dim=action_dim)
target_net.load_state_dict(policy_net.state_dict())
optimizer = optim.Adam(policy_net.parameters(), lr=LEARNING_RATE)
replay_buffer = deque(maxlen=REPLAY_BUFFER_SIZE)

# Generate random action compatible with the environment's dictionary action space
def generate_random_action():
    return {
        "active_chamber": {
            "paddle": (random.randint(0, 1), random.randint(0, 1)),
            "air_pump": random.randint(0, 1),
            "lid": random.randint(0, 1),
            "duration": random.randint(1, env.max_duration)
        },
        "curing_chamber": {
            "paddle": (random.randint(0, 1), random.randint(0, 1)),
            "air_pump": random.randint(0, 1),
            "lid": random.randint(0, 1),
            "duration": random.randint(1, env.max_duration)
        }
    }

# Choose action using epsilon-greedy strategy
def choose_action(state, epsilon):
    state_values = flatten_state(state)
    
    if random.random() < epsilon:
        return generate_random_action()
    else:
        with torch.no_grad():
            state_tensor = torch.FloatTensor(state_values).unsqueeze(0)
            q_values = policy_net(state_tensor)
            action_index = q_values.max(1)[1].item()
            return generate_random_action()  # Return random action for simplicity

# Sample from replay buffer
def sample_from_buffer(buffer, batch_size):
    batch = random.sample(buffer, batch_size)
    states, encoded_actions, rewards, next_states, dones = zip(*batch)

    # Extract a scalar or index from the encoded actions for indexing Q-values
    # Example: Using only the "air_pump" action as a scalar index for simplicity
    actions = torch.LongTensor([action[0][2] for action in encoded_actions])  # Just an example

    return (
        torch.FloatTensor(states),
        actions,
        torch.FloatTensor(rewards),
        torch.FloatTensor(next_states),
        torch.FloatTensor(dones),
    )


# Update the Q network
def update_model():
    if len(replay_buffer) < BATCH_SIZE:
        return

    # Sample from replay buffer and extract components
    states, actions, rewards, next_states, dones = sample_from_buffer(replay_buffer, BATCH_SIZE)
    
    # Get Q-values for the current policy network
    q_values = policy_net(states)  # Output shape [BATCH_SIZE, action_dim]

    # Use actions to gather specific Q-values from policy_net
    q_values = q_values.gather(1, actions.view(-1, 1).long()).squeeze(1)  # Shape [BATCH_SIZE]
    
    # Calculate next Q-values from target network
    next_q_values = target_net(next_states).max(1)[0]
    expected_q_values = rewards + (GAMMA * next_q_values * (1 - dones))

    # Compute loss and perform a backward pass
    loss = nn.MSELoss()(q_values, expected_q_values)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()



# Training loop
num_episodes = 500
epsilon = EPSILON_START

for episode in range(num_episodes):
    state = env.reset()
    total_reward = 0
    done = False

    while not done:
        action = choose_action(state, epsilon)
        next_state, reward, done, _ = env.step(action)
        total_reward += reward

        # Store encoded action
        replay_buffer.append((flatten_state(state), encode_action(action), reward, flatten_state(next_state), done))
        state = next_state

        update_model()

    if episode % TARGET_UPDATE_FREQUENCY == 0:
        target_net.load_state_dict(policy_net.state_dict())

    epsilon = max(EPSILON_END, epsilon * EPSILON_DECAY)

    print(f"Episode {episode+1}, Total Reward: {total_reward:.2f}")

print("Training complete.")
