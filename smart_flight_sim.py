import os
import sys
import time
import matplotlib

# Proper backend handling for BOTH local and CI/CD
if os.environ.get("CI") == "true":
    matplotlib.use("Agg")
    print("Using Matplotlib backend: Agg (CI/CD mode)")
else:
    for backend in ["MacOSX", "TkAgg", "Qt5Agg"]:
        try:
            matplotlib.use(backend)
            print(f"Using Matplotlib backend: {backend}")
            break
        except Exception:
            continue

import matplotlib.pyplot as plt
from geopy.distance import great_circle
import numpy as np
import csv
from tqdm import tqdm
import random


sys.stdout.reconfigure(line_buffering=True)

print("Initializing Smart Flight Autopilot Simulator...")


# Always use repo-relative logs folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

csv_path = os.path.join(LOG_DIR, "flight_data.csv")

print("Log path:", csv_path)


# Helper function for CI-safe plotting
def show_or_save(fig, filename):

    if os.environ.get("CI") == "true":

        filepath = os.path.join(LOG_DIR, filename)

        fig.savefig(filepath)

        print(f"Saved plot → {filepath}")

        plt.close(fig)

    else:

        plt.show()


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

        derivative = (error - self.prev_error) / dt if dt > 0 else 0

        output = (
            self.kp * error +
            self.ki * self.integral +
            self.kd * derivative
        )

        self.prev_error = error

        return output


# Flight route
start = (41.5325, -93.6480)
end = (41.9742, -87.9073)

distance_km = great_circle(start, end).km

target_altitude = 35000

altitude = 0
climb_rate = 0
dt = 1
steps = 180


pid = PID(0.4, 0.02, 0.15, target_altitude)

latitudes = np.linspace(start[0], end[0], steps)

longitudes = np.linspace(start[1], end[1], steps)


print(f"Route: Des Moines → Chicago ({distance_km:.1f} km)")


# Weather
weather_mode = random.choice(["Clear", "Windy", "Storm"])

if weather_mode == "Clear":

    wind_range = (-30, 30)
    turbulence_range = (-80, 80)

elif weather_mode == "Windy":

    wind_range = (-100, 100)
    turbulence_range = (-150, 150)

else:

    wind_range = (-200, 200)
    turbulence_range = (-300, 300)


print(f"Weather Mode: {weather_mode}")


with open(csv_path, "w", newline="") as csv_file:

    writer = csv.writer(csv_file)

    writer.writerow([
        "Step", "Latitude", "Longitude",
        "Altitude(ft)", "ClimbRate(ft/min)",
        "WindEffect", "Turbulence", "Weather"
    ])


    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))


    ax1.plot(longitudes, latitudes, "gray", linestyle="--", label="Flight Path")

    plane, = ax1.plot([], [], "ro", label="Aircraft")

    ax1.set_title("Smart Flight Navigation")

    ax1.legend()


    ax2.set_xlim(0, steps)

    ax2.set_ylim(0, target_altitude + 8000)

    alt_line, = ax2.plot([], [], "b-", label="Altitude")

    ax2.axhline(target_altitude, color="r", linestyle="--")

    ax2.legend()


    alt_history = []

    np.random.seed(42)

    print("\nTakeoff initiated...\n")


    for i in tqdm(range(steps), desc="Simulating Flight", ncols=80):

        wind_effect = np.random.uniform(*wind_range)

        turbulence = np.random.uniform(*turbulence_range)


        if i < steps * 0.3:

            pid.setpoint = target_altitude * (i / (steps * 0.3))

        elif i > steps * 0.8:

            pid.setpoint = target_altitude * (
                1 - (i - steps * 0.8) / (steps * 0.2)
            )

        else:

            pid.setpoint = target_altitude


        adjustment = pid.update(altitude + turbulence, dt)

        climb_rate += adjustment * 0.01

        altitude += climb_rate * (dt / 60)


        current_lat = latitudes[i] + wind_effect * 0.00001

        current_lon = longitudes[i] + wind_effect * 0.00002


        alt_history.append(altitude)

        writer.writerow([
            i + 1,
            current_lat,
            current_lon,
            altitude,
            climb_rate,
            wind_effect,
            turbulence,
            weather_mode
        ])


        plane.set_data([current_lon], [current_lat])

        alt_line.set_data(range(len(alt_history)), alt_history)


print("\nFlight complete")

print("Final Altitude:", altitude)

print("Saved CSV:", csv_path)


# Save or show plot
show_or_save(fig, "flight_simulation.png")

print("\nSimulation finished successfully.")