import math
import random

def get_desired_direction(agent, y_min, y_max):
    dir_x = 1.0 if agent.goal == 'r' else -1.0
    dir_y = 0.0
    
    # Wall steering
    dist_bottom = agent.position[1] - y_min
    if dist_bottom < agent.radius:
        dir_y += 5.0 * (agent.radius - dist_bottom)

    dist_top = y_max - agent.position[1]
    if dist_top < agent.radius:
        dir_y -= 5.0 * (agent.radius - dist_top)

    magnitude = math.sqrt(dir_x**2 + dir_y**2)
    if magnitude > 0:
        return [dir_x / magnitude, dir_y / magnitude]
    return [dir_x, 0.0]

def calculate_repulsive_force(agent, neighbors, decay_n, strength_A, body_k, slide_bias):
    total_force_x = 0.0
    total_force_y = 0.0
    
    speed = math.sqrt(agent.velocity[0]**2 + agent.velocity[1]**2)
    if speed > 0.1:
        heading_x, heading_y = agent.velocity[0] / speed, agent.velocity[1] / speed
    else:
        heading_x, heading_y = agent.desired_direction

    contact_margin = 0.15 

    for neighbor in neighbors:
        if agent.id == neighbor.id: continue
            
        dx = agent.position[0] - neighbor.position[0]
        dy = agent.position[1] - neighbor.position[1]
        dist = math.sqrt(dx**2 + dy**2)
        sum_radii = agent.radius + neighbor.radius
        
        if dist > sum_radii + 2.0: continue
        if dist < 0.01: dist = 0.01; dx = 0.01

        nx, ny = dx / dist, dy / dist
        tx, ty = ny, -nx 

        # Social Force
        if dist < sum_radii + 1.5 and dist > sum_radii + contact_margin:
            dot = (heading_x * -nx) + (heading_y * -ny)
            if dot > -0.5: 
                mag = strength_A * math.exp((sum_radii - dist) * decay_n)
                total_force_x += nx * mag + tx * (mag * slide_bias)
                total_force_y += ny * mag + ty * (mag * slide_bias)

        # Body Force
        threshold = sum_radii + contact_margin
        if dist < threshold:
            spring = body_k * (threshold - dist)
            slide = spring * slide_bias
            
            total_force_x += (nx * spring) + (tx * slide)
            total_force_y += (ny * spring) + (ty * slide)

    return [total_force_x, total_force_y]

def calculate_resistance_force(repulsive_force, gamma):
    fx, fy = repulsive_force
    mag = math.sqrt(fx**2 + fy**2)
    if mag < 0.001: return [0.0, 0.0]
    limit = min(math.exp(-gamma), mag)
    return [-fx/mag * limit, -fy/mag * limit]

def calculate_stochastic_force(probability_p):
    if random.random() > probability_p: return [0.0, 0.0]
    angle = random.uniform(0, 2 * math.pi)
    return [math.cos(angle), math.sin(angle)]