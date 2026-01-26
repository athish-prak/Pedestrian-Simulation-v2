import math
from model.forces import (
    get_desired_direction, 
    calculate_repulsive_force, 
    calculate_resistance_force, 
    calculate_stochastic_force
)

def update_agent_step(agent, neighbors, dt, y_min, y_max, 
                      density_alpha, random_prob, 
                      force_switch_ratio,
                      repulsion_A, decay_n, body_k, slide_bias,
                      resistance_gamma, perception_buffer_factor):
    
    # 1. Direction
    grad_dir = get_desired_direction(agent, y_min, y_max)
    agent.desired_direction = grad_dir 

    # 2. Forces
    agent_rep_force = calculate_repulsive_force(
        agent, neighbors, decay_n, repulsion_A, body_k, slide_bias
    )
    res_force = calculate_resistance_force(agent_rep_force, resistance_gamma)
    rand_force = calculate_stochastic_force(random_prob)

    env_force_x = agent_rep_force[0] + res_force[0] + rand_force[0]
    env_force_y = agent_rep_force[1] + res_force[1] + rand_force[1]

    # 3. Normalized State Switching
    implied_drive_limit = agent.desired_speed / dt
    total_force_mag = math.sqrt(env_force_x**2 + env_force_y**2)
    force_ratio = total_force_mag / implied_drive_limit
    
    agent.under_pressure = (force_ratio > force_switch_ratio)

    # 4. Pressure Yielding (Derived from Speed/dt)
    current_desired_speed = agent.desired_speed
    opposition = -(env_force_x * grad_dir[0] + env_force_y * grad_dir[1])
    
    if opposition > 0:
        opp_ratio = opposition / implied_drive_limit
        yield_start = 0.5
        yield_stop = 2.0
        
        if opp_ratio > yield_start:
            fraction = (opp_ratio - yield_start) / (yield_stop - yield_start)
            if fraction > 1.0: fraction = 1.0
            current_desired_speed *= (1.0 - fraction)

    # 5. Integration
    drive_x = current_desired_speed * grad_dir[0]
    drive_y = current_desired_speed * grad_dir[1]
    
    velocity_x = drive_x + (env_force_x * dt)
    velocity_y = drive_y + (env_force_y * dt)
    
    speed_mag = math.sqrt(velocity_x**2 + velocity_y**2)
    max_speed = agent.desired_speed * 1.5
    if speed_mag > max_speed:
        scale = max_speed / speed_mag
        velocity_x *= scale
        velocity_y *= scale

    next_x = agent.position[0] + velocity_x * dt
    next_y = agent.position[1] + velocity_y * dt
    
    if next_y < agent.radius: next_y = agent.radius
    if next_y > y_max - agent.radius: next_y = y_max - agent.radius
    
    agent.position[0] = next_x
    agent.position[1] = next_y
    agent.velocity = [velocity_x, velocity_y]
    agent.speed = speed_mag