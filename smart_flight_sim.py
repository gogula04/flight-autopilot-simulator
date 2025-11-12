import os
import sys
import time
import matplotlib

#  Automatically detect a GUI backend (macOS / Linux / Windows)
for backend in ["MacOSX", "TkAgg", "Qt5Agg"]:
    try:
        matplotlib.use(backend)
        print(f" Using Matplotlib backend: {backend}")
        break
    except Exception as e:
        print(f" Failed to use backend {backend}: {e}")

import matplotlib.pyplot as plt
from geopy.distance import great_circle
import numpy as np
import csv
from tqdm import tqdm
import random

sys.stdout.reconfigure(line_buffering=True)
print(" Initializing Smart Flight Autopilot Simulator...")

os.makedirs("logs", exist_ok=True)
csv_path = os.path.join("logs", "flight_data.csv")
print(" Log path:", os.path.abspath(csv_path))



class PID:
    def __init__(self, kp, ki, kd, setpoint):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.integral = 0
        self.prev_error = 0

    def update(self, current_value, dt):
        error = self.setpoint - current_value
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.prev_error = error
        return output


start = (41.5325, -93.6480)  # Des Moines
end = (41.9742, -87.9073)    # Chicago
distance_km = great_circle(start, end).km

target_altitude = 35000
altitude = 0
climb_rate = 0
dt = 1
steps = 180  

pid = PID(0.4, 0.02, 0.15, target_altitude)
latitudes = np.linspace(start[0], end[0], steps)
longitudes = np.linspace(start[1], end[1], steps)

print(f" Route: Des Moines → Chicago ({distance_km:.1f} km)")



weather_mode = random.choice(["Clear", "Windy", "Storm"])
if weather_mode == "Clear":
    wind_range = (-30, 30)
    turbulence_range = (-80, 80)
elif weather_mode == "Windy":
    wind_range = (-100, 100)
    turbulence_range = (-150, 150)
else:  # Storm
    wind_range = (-200, 200)
    turbulence_range = (-300, 300)

print(f" Weather Mode: {weather_mode}")



with open(csv_path, "w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow([
        "Step", "Latitude", "Longitude", "Altitude(ft)", "ClimbRate(ft/min)",
        "WindEffect", "Turbulence", "Weather"
    ])

  
    plt.ion()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    try:
        fig.canvas.manager.set_window_title("Smart Flight Autopilot Simulator")
    except Exception:
        pass

   
    ax1.plot(longitudes, latitudes, "gray", linestyle="--", label="Flight Path")
    plane, = ax1.plot([], [], "ro", label="Aircraft")
    ax1.set_xlabel("Longitude")
    ax1.set_ylabel("Latitude")
    ax1.legend()
    ax1.set_title(" Smart Flight Navigation")

    
    ax2.set_xlim(0, steps)
    ax2.set_ylim(0, target_altitude + 8000)
    alt_line, = ax2.plot([], [], "b-", label="Altitude")
    ax2.axhline(y=target_altitude, color="r", linestyle="--", label="Target Altitude")
    ax2.set_xlabel("Time Step")
    ax2.set_ylabel("Altitude (ft)")
    ax2.legend()
    ax2.set_title(" Autopilot Altitude Control")

    alt_history = []
    np.random.seed(42)
    print("\n🛫 Takeoff initiated... Engines stable. Climbing to cruising altitude.\n")

    
    for i in tqdm(range(steps), desc=" Simulating Flight", ncols=80):
        
        wind_effect = np.random.uniform(*wind_range)
        turbulence = np.random.uniform(*turbulence_range)

        
        if i < steps * 0.3:
            pid.setpoint = target_altitude * (i / (steps * 0.3))   # takeoff climb
        elif i > steps * 0.8:
            pid.setpoint = target_altitude * (1 - (i - steps * 0.8) / (steps * 0.2))  # landing descent
        else:
            pid.setpoint = target_altitude  # cruise

        #  PID Control
        adjustment = pid.update(altitude + turbulence, dt)
        climb_rate += adjustment * 0.01
        altitude += climb_rate * (dt / 60)

        #  Wind drift
        current_lat = latitudes[i] + (wind_effect * 0.00001)
        current_lon = longitudes[i] + (wind_effect * 0.00002)

        #  Log Data
        alt_history.append(altitude)
        writer.writerow([
            i + 1, current_lat, current_lon, altitude, climb_rate, wind_effect, turbulence, weather_mode
        ])

        #  Update visualization
        plane.set_data([current_lon], [current_lat])
        alt_line.set_data(range(len(alt_history)), alt_history)

        # Dashboard Overlay
        ax2.texts.clear()
        phase = (
            " Takeoff" if i < steps * 0.3 else
            " Cruise" if i < steps * 0.8 else
            "Landing"
        )
        ax2.text(
            5, target_altitude + 4000,
            f"Phase: {phase}\nAltitude: {altitude:,.0f} ft\nClimb Rate: {climb_rate:,.0f} ft/min\n"
            f"Wind: {wind_effect:+.1f}\nTurb: {turbulence:+.1f}\nWeather: {weather_mode}",
            fontsize=10, bbox=dict(facecolor='white', alpha=0.7)
        )

        plt.pause(0.05)

    print("\n Flight complete — Autopilot maintained stability through turbulence.\n")

plt.ioff()
print(" Flight Summary")
print("---------------------------")
print(f" Total Distance: {distance_km:.1f} km")
print(f" Target Altitude: {target_altitude} ft")
print(f" Final Altitude: {altitude:.1f} ft")
print(f" Avg climb rate (last phase): {np.mean(alt_history[-20:]):.2f} ft/min")
print(f" Weather Mode: {weather_mode}")
print(f" Data saved to: {csv_path}")

print("\n Simulation finished — window will stay open until you close it.")
plt.show(block=True)
