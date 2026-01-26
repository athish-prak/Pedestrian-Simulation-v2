import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
import matplotlib.patches as mpatches
from utils.engine import Engine

class Simulation:
    def __init__(self, config):
        self.cfg = config
        self.engine = Engine(config)
        
        # Setup Figure
        self.fig, self.ax = plt.subplots(figsize=(14, 7))
        self.ax.set_xlim(0, config.CORRIDOR_LENGTH_METERS)
        self.ax.set_ylim(-1, config.CORRIDOR_WIDTH_METERS + 1)
        self.ax.set_aspect('equal')
        
        # Simple Title and Labels
        self.ax.set_title("Pedestrian Simulation", fontsize=16, pad=20)
        self.ax.set_xlabel("Corridor Length (meters)")
        self.ax.set_ylabel("Width (meters)")
        
        # Draw Walls
        self.ax.axhline(0, color='#333333', linewidth=4)
        self.ax.axhline(config.CORRIDOR_WIDTH_METERS, color='#333333', linewidth=4)
        
        # Grid
        self.ax.grid(True, linestyle='--', alpha=0.3)

        # Legend
        red_patch = mpatches.Patch(color='firebrick', label='Right Goal')
        blue_patch = mpatches.Patch(color='royalblue', label='Left Goal')
        self.ax.legend(handles=[red_patch, blue_patch], loc='upper right')

        # Stats Box
        self.time_text = self.ax.text(
            0.02, 0.95, '', transform=self.ax.transAxes, 
            fontsize=12, verticalalignment='top', 
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8)
        )
        
        self.circles = {} 

    def update(self, frame):
        self.engine.step()
        
        # Sync Visualization
        current_ids = set(a.id for a in self.engine.agents)
        active_ids = list(self.circles.keys())
        
        # Remove finished
        for ag_id in active_ids:
            if ag_id not in current_ids:
                self.circles[ag_id].remove()
                del self.circles[ag_id]
        
        # Update or Create
        for agent in self.engine.agents:
            # Simple Static Colors
            color = 'firebrick' if agent.goal == 'r' else 'royalblue'

            if agent.id in self.circles:
                c = self.circles[agent.id]
                c.center = agent.position
                c.set_facecolor(color)
            else:
                c = Circle(
                    agent.position, 
                    agent.radius, 
                    facecolor=color, 
                    edgecolor='white',
                    linewidth=0.5,
                    alpha=0.9
                )
                self.ax.add_patch(c)
                self.circles[agent.id] = c
        
        # Update Stats
        stats = (
            f"Time: {self.engine.sim_time:.2f} s\n"
            f"Active Agents: {len(self.engine.agents)}\n"
            f"Finished: {self.engine.agents_finished}"
        )
        self.time_text.set_text(stats)
                
        return list(self.circles.values()) + [self.time_text]

    def run(self):
        anim = FuncAnimation(
            self.fig, 
            self.update, 
            frames=None, 
            # Increased interval to slow down animation
            # 50ms = 20 FPS (Slower and smoother to watch)
            interval=50, 
            blit=True
        )
        plt.show()