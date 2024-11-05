Test Case 1:
1. Simulate an action where either the paddle or air pump is activated.
2. Ensure that the environment state updates after the action.
3. Check if the reward is calculated correctly.
4. Verify if the episode is marked AS complete based on the updated state.


此测试的作用：
1. **初始重置**：调用 `env.reset()` 后打印初始状态。
2. **桨动作**：发送测试动作，桨运行 5 秒，气泵也运行 5 秒。
3. **打印更新状态**：显示应用操作后状态如何变化。
4. **自然变化**：调用 `step(None)` 来模拟没有任何操作的时间步骤，仅应用自然变化。
5. **情节检查**：根据更新的状态验证情节是否已完成。

### 预期输出：
- **初始状态**：任何操作之前的初始温度、气体和其他值。
- **更新状态**：状态应显示基于操作的温度、气体水平（例如二氧化碳、甲烷、氧气）和其他变量的变化。
- **奖励**：基于当前状态与最佳条件的接近程度的奖励值。
- **情节完成**：情节是否由于温度超过限制等条件而结束。

import numpy as np

# Initialize your composting environment
env = CompostingEnv()

# Reset the environment to start a new episode
initial_state = env.reset()
print("Initial State:", initial_state)

# Define a simple test action for the paddle (motor ID 0) and air pump (motor ID 1)
test_action_paddle = {
    "motor": {
        "id": 0,  # Paddle action
        "duration_sec": np.array([5.0], dtype=np.float32)  # 5 seconds of paddle movement
    },
    "actions": [
        {
            "type": 0,  # Air pump action
            "id": 1,  # Air pump ID
            "duration_ms": np.array([5000], dtype=np.float32)  # 5 seconds of air pump operation
        }
    ]
}

# Call the step function with the test action
state, reward, done, info = env.step(test_action_paddle)

# Print the results after taking the action
print("Updated State after Paddle Action:", state)
print("Reward:", reward)
print("Episode Done:", done)

# Check natural changes by stepping without any action
state, reward, done, info = env.step(None)
print("\nState after Natural Changes:", state)
print("Reward after Natural Changes:", reward)
print("Episode Done:", done)

