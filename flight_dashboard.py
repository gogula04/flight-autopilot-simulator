import os
import subprocess
import time
import sys
import platform
import matplotlib.pyplot as plt


print("==============================================")
print("     SMART FLIGHT AUTOPILOT CONTROL SUITE")
print("==============================================\n")


BASE_DIR = os.path.expanduser("~/Documents/flight_autopilot_sim")
LOG_PATH = os.path.join(BASE_DIR, "logs", "flight_data.csv")
SCRIPTS = {
    "Simulation": os.path.join(BASE_DIR, "smart_flight_sim.py"),
    "Analysis": os.path.join(BASE_DIR, "analyze_flight_data.py"),
    "Flight Path": os.path.join(BASE_DIR, "flight_plot.py"),
}


if not os.path.exists(BASE_DIR):
    print(f" Project folder not found: {BASE_DIR}")
    sys.exit(1)

if not os.path.exists(SCRIPTS["Simulation"]):
    print(" Missing smart_flight_sim.py — please add it.")
    sys.exit(1)

os.makedirs(os.path.join(BASE_DIR, "logs"), exist_ok=True)


print(" Launching Smart Flight Simulation...\n")
start_time = time.time()
subprocess.run([sys.executable, SCRIPTS["Simulation"]])
print(f"\n Simulation finished in {time.time() - start_time:.1f} seconds.\n")


if not os.path.exists(LOG_PATH):
    print(" No flight_data.csv log found! Simulation may have failed.")
    sys.exit(1)


print(" Running Flight Data Analysis...\n")
subprocess.run([sys.executable, SCRIPTS["Analysis"]])

print("\n Opening Flight Path Visualization...\n")
subprocess.run([sys.executable, SCRIPTS["Flight Path"]])


print("\n FLIGHT AUTOPILOT DASHBOARD COMPLETE")
print("───────────────────────────────────────")
print(f" Logs saved at: {LOG_PATH}")
print(f" System: {platform.system()} {platform.release()}")
print(f" Execution time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
print("───────────────────────────────────────")
print(" Flight simulation, analysis, and visualization done!\n")

time.sleep(3)
plt.close("all")
