# Smart Flight Autopilot Simulator

The Smart Flight Autopilot Simulator is a Python-based project that models an automated aircraft control system using a PID (Proportional–Integral–Derivative) controller. The simulator replicates the process of stabilizing a plane’s altitude during a flight from Des Moines to Chicago, logs real-time flight data, and visualizes key performance metrics such as altitude, climb rate, and turbulence effects.

---

## Overview

This project demonstrates how an autopilot system adjusts the aircraft’s climb rate and altitude dynamically using PID feedback control. It also integrates data visualization and analysis features, allowing users to observe flight behavior through live charts and saved CSV logs.

The simulator was developed for learning and experimentation purposes, focusing on control systems, data analysis, and graphical visualization in Python.

---

## Features

- Implements a PID controller to automatically stabilize flight altitude.
- Simulates a flight route from Des Moines, Iowa to Chicago, Illinois.
- Logs flight telemetry such as altitude, climb rate, turbulence, and wind variations.
- Provides real-time visualization of the flight path and altitude changes.
- Generates analytical graphs for post-flight performance review.

---

## Project Structure

flight_autopilot_sim/
│
├── smart_flight_sim.py # Main simulator script (autopilot and logging)
├── analyze_flight_data.py # Post-flight analytics and performance visualization
├── flight_plot.py # Basic visualization of the flight path
├── autopilot_pid.py # PID control logic
├── flight_dashboard.py # Optional dashboard view (for extended visualization)
│
├── logs/
│ └── flight_data.csv # Logged flight data
│
└── venv/ # Virtual environment (excluded from repository)

Copy code



---

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/gogula04/flight-autopilot-simulator.git
   cd flight-autopilot-simulator
2. Create and activate a virtual environment:
       python3 -m venv venv
       source venv/bin/activate   # On macOS or Linux

3. Install the required dependencies:
      pip install -r requirements.txt
      If you don’t have a requirements.txt file, install the main packages manually:
      pip install matplotlib numpy geopy tqdm pandas

How to Run
1. Run the main flight simulation
python3 smart_flight_sim.py
This script initializes the PID controller, simulates a full flight from Des Moines to Chicago, and logs the data to logs/flight_data.csv.

2. Analyze the flight data
python3 analyze_flight_data.py
This script reads the flight log and generates visual graphs such as altitude stability, climb rate vs. turbulence, and altitude distribution.

3. View the flight path (optional)
python3 flight_plot.py
Displays a simple map of the simulated flight route.

Example Output
After running the simulation, the project will produce:
A CSV file (logs/flight_data.csv) containing all recorded telemetry data.
Graphical plots showing:
Altitude vs. Time (stability over the course of flight)
Climb Rate vs. Turbulence (effect of environmental conditions)
Altitude distribution histogram
These outputs demonstrate how the autopilot system reacts to dynamic changes and reaches the target altitude efficiently.

Technologies Used
Python 3.14
Matplotlib for real-time plotting and visualization
NumPy for numerical computations
GeoPy for calculating great-circle distances
Pandas for data analysis
TQDM for progress visualization

Author
Venkatesh Gogula
Computer Science Major
Iowa State University, Ames, Iowa
GitHub: gogula04

License
This project is released under the MIT License. You are free to use, modify, and distribute it for educational and research purposes.
