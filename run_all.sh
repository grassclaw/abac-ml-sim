#!/bin/bash

# run_all.sh
# Launches the ABAC ML simulation environment (Flask + Streamlit)

# Step 1: Enrich synthetic data
echo "[+] Enriching data..."
python3 scripts/enrich_data.py || { echo "[!] Enrich failed"; exit 1; }

# Step 2: Train the model
echo "[+] Training model..."
python3 scripts/train_model.py || { echo "[!] Model training failed"; exit 1; }

# Step 3: Launch Flask API in background
echo "[+] Starting ABAC model API (Flask)..."
python3 scripts/live_abac_checker.py &
FLASK_PID=$!
echo "    Flask PID: $FLASK_PID"

# Step 4: Launch Streamlit dashboard in background
echo "[+] Launching Streamlit dashboard..."
streamlit run scripts/dashboard.py &
DASH_PID=$!
echo "    Dashboard PID: $DASH_PID"

# Step 5: Display instructions for CLI (to run manually)
echo ""
echo "[✔] Environment ready. Use a second terminal to test live ABAC decisions:"
echo "    python3 scripts/abac_cli_test.py"
echo ""
echo "[!] Press Ctrl+C here to stop Flask and Streamlit when you're done."

# Wait for background jobs to keep the script alive
wait $FLASK_PID $DASH_PID