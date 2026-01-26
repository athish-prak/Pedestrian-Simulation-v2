import random
from model.agent import Agent
from model.update import update_agent_step

class Engine:
    def __init__(self, config):
        self.cfg = config
        self.agents = []
        self.sim_time = 0.0
        self.dt = config.TIME_STEP_SECONDS
        
        self.agent_id_counter = 0
        self.spawn_timer = 0.0
        
        rate = getattr(config, 'AGENT_INJECTION_RATE_PER_SEC', 2.0)
        self.spawn_interval = 1.0 / rate if rate > 0 else 1.0
        self.agents_spawned = 0
        self.agents_finished = 0

    def step(self):
        # Spawn
        if self.agents_spawned < self.cfg.TOTAL_AGENTS_TO_SPAWN:
            self.spawn_timer += self.dt
            if self.spawn_timer >= self.spawn_interval:
                self.spawn_timer = 0.0
                self._spawn_agent()

        # Update
        current_agents = list(self.agents)
        for agent in current_agents:
            update_agent_step(
                agent=agent, 
                neighbors=current_agents,
                dt=self.dt, 
                y_min=0.0, 
                y_max=self.cfg.CORRIDOR_WIDTH_METERS,
                density_alpha=self.cfg.DENSITY_SPEED_PENALTY_ALPHA, 
                random_prob=self.cfg.RANDOM_FORCE_PROBABILITY,
                force_switch_ratio=self.cfg.FORCE_SWITCH_RATIO,
                repulsion_A=self.cfg.REPULSION_FORCE_MAGNITUDE_A, 
                decay_n=self.cfg.REPULSION_DECAY_COEFFICIENT_N,
                body_k=self.cfg.BODY_FORCE_CONSTANT_K,
                slide_bias=self.cfg.SLIDING_BIAS_FACTOR,
                resistance_gamma=self.cfg.RESISTANCE_FORCE_COEFFICIENT_GAMMA,
                perception_buffer_factor=self.cfg.PERCEPTION_BUFFER_FACTOR
            )

        # Cleanup
        active = []
        for ag in self.agents:
            finished = False
            if ag.goal == 'r' and ag.position[0] >= self.cfg.CORRIDOR_LENGTH_METERS:
                finished = True
            elif ag.goal == 'l' and ag.position[0] <= 0.0:
                finished = True
            
            if finished:
                self.agents_finished += 1
            else:
                active.append(ag)
        self.agents = active
        self.sim_time += self.dt

    def _spawn_agent(self):
        goal = 'r' if random.random() < 0.5 else 'l'
        radius = self.cfg.AGENT_RADIUS
        y_pos = random.uniform(radius + 0.1, self.cfg.CORRIDOR_WIDTH_METERS - radius - 0.1)
        x_pos = 0.5 if goal == 'r' else self.cfg.CORRIDOR_LENGTH_METERS - 0.5
        
        speed = random.gauss(self.cfg.AGENT_DESIRED_SPEED_MEAN, self.cfg.AGENT_DESIRED_SPEED_STD)
        speed = max(0.5, min(speed, 2.5))

        new_agent = Agent(self.agent_id_counter, [x_pos, y_pos], goal, speed, radius)
        self.agents.append(new_agent)
        self.agent_id_counter += 1
        self.agents_spawned += 1