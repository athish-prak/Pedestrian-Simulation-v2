# Pedestrian Flow Simulation

## Overview
A physics-based simulation of crowd dynamics in a confined corridor. This model goes beyond standard repulsion logic by implementing "Pressure Yielding" and "Contact Friction," simulating how agents physically struggle and slow down in dense crowds.

## Architecture
* **`config.yaml`**: Central control for physics parameters, spawn rates, and geometry.
* **`utils/engine.py`**: The headless physics solver (calculates positions/velocities).
* **`utils/visualizer.py`**: The Matplotlib renderer that displays the simulation.
* **`model/`**: Contains the core logic for agent states, force calculations, and integration steps.

## Physics Model
The agents move based on a hybrid force calculation:
1.  **Social Repulsion:** Agents steer away from each other before contact.
2.  **Contact Friction:** A "gritty" sliding mechanic (Bias Factor 0.25) preventing unrealistic frictionless sliding.
3.  **Pressure Yielding:** If external forces (crowd crush) exceed 40% of an agent's drive capability, the agent voluntarily reduces its desired speed, simulating resignation under pressure.

## Emergent Phenomena
* **Lane Formation:** Spontaneous organization of directional flow.
* **Stop-and-Go Waves:** Agents yielding under pressure cause realistic backward-propagating slowdowns.
* **Friction Locking:** Agents passing in tight quarters momentarily "stick" rather than bouncing off perfectly.

## How to Run Experiments
1.  **Run Visual:** Execute `python main.py` to watch the crowd behavior.
2.  **Headless Mode:** Import `Engine` directly in Python scripts to run fast, non-visual batches for data collection.
3.  **Tuning:** Adjust `AGENT_INJECTION_RATE` or `FORCE_SWITCH_RATIO` in `config.yaml` to stress-test the crowd stability.
