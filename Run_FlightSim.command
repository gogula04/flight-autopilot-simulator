#!/bin/bash
cd ~/Documents/flight_autopilot_sim
source venv/bin/activate

echo "🚀 Launching Smart Flight Autopilot Simulator (GUI enabled)..."
python3 smart_flight_sim.py

echo ""
echo "✅ Simulation finished. Press ENTER to close this window."
read


