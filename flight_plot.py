import matplotlib.pyplot as plt
from geopy.distance import great_circle
import numpy as np
import time


start = (41.5325, -93.6480)
end = (41.9742, -87.9073)


distance_km = great_circle(start, end).km
speed_kmh = 800  
total_time_hr = distance_km / speed_kmh
total_seconds = total_time_hr * 3600
steps = 150
update_interval = total_seconds / steps / 50  

print(" Flight Path Visualizer")
print("----------------------------")
print(f"From: Des Moines (IA)")
print(f"To:   Chicago (IL)")
print(f"Total Distance: {distance_km:.1f} km")
print(f"Estimated Flight Time: {total_time_hr*60:.1f} minutes\n")


latitudes = np.linspace(start[0], end[0], steps)
longitudes = np.linspace(start[1], end[1], steps)


plt.ion()
fig, ax = plt.subplots(figsize=(8, 6))
fig.canvas.manager.set_window_title("Flight Path Visualizer")

ax.plot(longitudes, latitudes, "gray", linestyle="--", linewidth=1.5, label="Route Path")
plane, = ax.plot([], [], "ro", markersize=8, label="Aircraft")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_title(" Flight Path: Des Moines → Chicago")
ax.legend()
ax.grid(True, linestyle="--", alpha=0.6)


distance_covered = []
time_start = time.time()

for i in range(steps):
    
    current_pos = (latitudes[i], longitudes[i])
    progress_km = great_circle(start, current_pos).km
    distance_covered.append(progress_km)
    elapsed = time.time() - time_start
    eta_min = max((total_seconds - elapsed) / 60, 0)

    
    plane.set_data([longitudes[i]], [latitudes[i]])


    ax.texts.clear()
    ax.text(
        longitudes[i], latitudes[i] + 0.05,
        f" {progress_km:.1f} km / {distance_km:.1f} km\n"
        f" ETA: {eta_min:.1f} min",
        fontsize=9, bbox=dict(facecolor="white", alpha=0.7)
    )

    plt.pause(update_interval)

print(" Flight completed successfully!")
print(f"Total Distance Flown: {distance_km:.1f} km")
print(f"Elapsed Simulation Time: {(time.time() - time_start):.1f} sec")

plt.ioff()
ax.text(
    end[1], end[0],
    " Arrived at Chicago",
    fontsize=10, color="green", weight="bold",
    bbox=dict(facecolor="white", alpha=0.8)
)
plt.show()
