import matplotlib
matplotlib.use("MacOSX")  # ✅ Force native macOS GUI backend


import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- Detect and Load Latest Flight Data ---
log_path = "logs/flight_data.csv"
if not os.path.exists(log_path):
    print("⚠️ No flight log found. Please run 'smart_flight_sim.py' first.")
    exit()

data = pd.read_csv(log_path)
print(f"📂 Loaded flight data: {len(data)} records from '{log_path}'")

# --- Compute Key Metrics ---
avg_climb = data["ClimbRate(ft/min)"].mean()
max_alt = data["Altitude(ft)"].max()
min_alt = data["Altitude(ft)"].min()
overshoot = max_alt - 35000
turbulence_std = np.std(data["Turbulence"])
avg_turb = data["Turbulence"].mean()
final_alt = data["Altitude(ft)"].iloc[-1]
weather_mode = data["Weather"].iloc[0] if "Weather" in data.columns else "Unknown"

# --- Print Summary ---
print("\n✈️  FLIGHT PERFORMANCE ANALYSIS")
print("──────────────────────────────────────────────")
print(f"🌤️  Weather Mode: {weather_mode}")
print(f"📈  Average Climb Rate: {avg_climb:.2f} ft/min")
print(f"🧭  Maximum Altitude: {max_alt:.1f} ft")
print(f"🪂  Minimum Altitude: {min_alt:.1f} ft")
print(f"🎯  Target Altitude: 35000 ft")
print(f"📊  Overshoot Above Target: {overshoot:.1f} ft")
print(f"🌪️  Turbulence Variability (σ): {turbulence_std:.1f}")
print(f"🌡️  Average Turbulence: {avg_turb:.1f}")
print(f"🏁  Final Altitude: {final_alt:.1f} ft")
print("──────────────────────────────────────────────")

# --- Plot Altitude over Time ---
plt.figure(figsize=(10, 5))
plt.plot(data["Step"], data["Altitude(ft)"], label="Altitude", color="blue", linewidth=2)
plt.axhline(35000, color="r", linestyle="--", label="Target Altitude (35,000 ft)")
plt.fill_between(data["Step"], data["Altitude(ft)"], 35000, where=(data["Altitude(ft)"] > 35000),
                 color="red", alpha=0.1, interpolate=True, label="Overshoot Zone")
plt.title("✈️ Autopilot Altitude Stability")
plt.xlabel("Time Step")
plt.ylabel("Altitude (ft)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()

# --- Plot Climb Rate vs Turbulence ---
plt.figure(figsize=(10, 5))
plt.plot(data["Step"], data["ClimbRate(ft/min)"], label="Climb Rate (ft/min)", color="green", linewidth=1.8)
plt.plot(data["Step"], data["Turbulence"], label="Turbulence", color="orange", alpha=0.7)
plt.title("🌀 Climb Rate vs Turbulence")
plt.xlabel("Time Step")
plt.ylabel("Value")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()

# --- Optional: Altitude Distribution Histogram ---
plt.figure(figsize=(8, 4))
plt.hist(data["Altitude(ft)"], bins=20, color="skyblue", edgecolor="black", alpha=0.8)
plt.title("📊 Altitude Distribution During Flight")
plt.xlabel("Altitude (ft)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

print("\n✅ Analysis complete — all graphs displayed successfully.")
