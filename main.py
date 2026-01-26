import yaml
from utils.visualizer import Simulation

# Helper to access dict as obj
class ConfigWrapper:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            setattr(self, key, value)

if __name__ == "__main__":
    with open("config.yaml", 'r') as stream:
        config_dict = yaml.safe_load(stream)
    
    cfg = ConfigWrapper(config_dict)
    sim = Simulation(cfg)
    sim.run()