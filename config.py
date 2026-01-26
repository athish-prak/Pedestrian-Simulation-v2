class SimulationConfig:
    # --- TIME & SPACE ---
    TIME_STEP_SECONDS = 0.05
    CORRIDOR_WIDTH_METERS = 10.0
    CORRIDOR_LENGTH_METERS = 20.0
    TOTAL_SIMULATION_TIME = 100.0

    # --- AGENT SPAWNING ---
    TOTAL_AGENTS_TO_SPAWN = 100
    AGENT_INJECTION_RATE_PER_SEC = 2.0  # Agents per second
    
    # --- AGENT PROPERTIES ---
    AGENT_RADIUS = 0.3
    # Speed (Normal Distribution)
    AGENT_DESIRED_SPEED_MEAN = 1.34
    AGENT_DESIRED_SPEED_STD = 0.26
    PERCEPTION_BUFFER_FACTOR = 1.0

    # --- PHYSICS PARAMETERS (TUNED) ---
    
    # 1. Repulsion (Social Force)
    REPULSION_FORCE_MAGNITUDE_A = 4.0
    REPULSION_DECAY_COEFFICIENT_N = 2.0 
    
    # 2. Body Force (Physical Contact)
    # Stiff spring to prevent overlap
    BODY_FORCE_CONSTANT_K = 1200.0   
    
    # 3. Sliding Friction (The "Gritty" Logic)
    # 0.25 means 25% of push force becomes slide force.
    SLIDING_BIAS_FACTOR = 0.25       

    # 4. Other Forces
    RESISTANCE_FORCE_COEFFICIENT_GAMMA = 0.2 # Damping
    FORCE_SWITCHING_THRESHOLD = 0.5
    RANDOM_FORCE_PROBABILITY = 0.1  # Low noise
    
    # 5. Density (Handled by Pressure Yielding now, so 0)
    DENSITY_SPEED_PENALTY_ALPHA = 0.0