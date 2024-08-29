class CompostingEnv(gym.Env):
    def __init__(self):
        super(CompostingEnv, self).__init__()

        # Define structured observation space
        self.observation_space = spaces.Dict({
            "temperature_active": spaces.Box(low=0, high=100, shape=(4,), dtype=np.float32),
            "temperature_curing": spaces.Box(low=0, high=100, shape=(2,), dtype=np.float32),
            "moisture_active": spaces.Box(low=0, high=100, shape=(2,), dtype=np.float32),
            "moisture_curing": spaces.Box(low=0, high=100, shape=(2,), dtype=np.float32),
            "gases": spaces.Dict({
                "co2": spaces.Box(low=0, high=100, shape=(1,), dtype=np.float32),
                "oxygen": spaces.Box(low=0, high=100, shape=(1,), dtype=np.float32),
                "methane": spaces.Box(low=0, high=100, shape=(1,), dtype=np.float32)
            }),
        })
        
       # Define the action space with duration for motor and air pump actions
        self.action_space = spaces.Dict({
            "motor": spaces.Dict({
                "id": spaces.Discrete(2),  # Motor ID: 0, 1
                "duration_ms": spaces.Box(low=0, high=10000, shape=(1,), dtype=np.float32)
            }),
            "actions": spaces.Tuple([
                spaces.Dict({
                    "type": spaces.Discrete(1),  # Only 1 type here for air_pump
                    "id": spaces.Discrete(2),  # Air pump ID: 0, 1
                    "duration_ms": spaces.Box(low=0, high=10000, shape=(1,), dtype=np.float32)
                }),
                spaces.Dict({
                    "type": spaces.Discrete(1),  # Only 1 type here for air_pump
                    "id": spaces.Discrete(2),  # Air pump ID: 0, 1
                    "duration_ms": spaces.Box(low=0, high=10000, shape=(1,), dtype=np.float32)
                })
            ])
        })
        
         # Initialize state and any other necessary variables
        self.state = self.reset()
