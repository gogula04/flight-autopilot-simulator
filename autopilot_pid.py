import time
import matplotlib.pyplot as plt
import numpy as np

class PID:
    def __init__(self, kp, ki, kd, setpoint):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.integral = 0
        self.prev_error = 0

    def update(self, current_value, dt):
        """Compute PID output for a given process variable."""
        error = self.setpoint - current_value
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.prev_error = error
        return output


target_altitude = 35000      
altitude = 0                  
climb_rate = 0                
dt = 1                        
total_time = 600              
turbulence = True             

pid = PID(kp=0.4, ki=0.02, kd=0.15, setpoint=target_altitude)


times = []
altitudes = []
climb_rates = []
errors = []

print(" Autopilot PID Altitude Control Simulation")
print("──────────────────────────────────────────────")

for t in range(total_time):
    noise = np.random.uniform(-100, 100) if turbulence else 0
    sensed_altitude = altitude + noise

    adjustment = pid.update(sensed_altitude, dt)
    climb_rate += adjustment * 0.01
    altitude += climb_rate * (dt / 60)

    times.append(t)
    altitudes.append(altitude)
    climb_rates.append(climb_rate)
    errors.append(pid.setpoint - altitude)

    if t % 10 == 0 or t == total_time - 1:
        print(f" {t:3d}s | Altitude: {altitude:8.1f} ft | Climb Rate: {climb_rate:7.1f} ft/min | Error: {pid.setpoint - altitude:8.1f}")

print("\n Simulation complete.")
print(f"Final Altitude: {altitude:.1f} ft (Target: {target_altitude} ft)")
print(f"Max Overshoot: {max(altitudes) - target_altitude:.1f} ft")
print(f"Mean Error: {np.mean(np.abs(errors)):.1f} ft\n")

plt.figure(figsize=(10, 5))
plt.plot(times, altitudes, color="blue", label="Altitude (ft)")
plt.axhline(y=target_altitude, color="r", linestyle="--", label="Target Altitude (35,000 ft)")
plt.title(" Autopilot Altitude Control (PID Response)")
plt.xlabel("Time (seconds)")
plt.ylabel("Altitude (ft)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 4))
plt.plot(times, errors, color="orange", label="Altitude Error (ft)")
plt.axhline(0, color="black", linewidth=1)
plt.title(" PID Error Convergence")
plt.xlabel("Time (seconds)")
plt.ylabel("Error (ft)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()
