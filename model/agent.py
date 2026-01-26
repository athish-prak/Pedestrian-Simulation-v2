class Agent:
    def __init__(self, id, position, goal, desired_speed, radius):
        self.id = id
        self.position = list(position)
        self.velocity = [0.0, 0.0]
        self.goal = goal # 'r' or 'l'
        
        self.desired_speed = desired_speed
        self.radius = radius
        
        # Internal state
        self.desired_direction = [0.0, 0.0]
        self.speed = 0.0
        self.under_pressure = False