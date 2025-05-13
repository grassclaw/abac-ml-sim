#!/bin/bash

# run_once.sh
# One-pass execution of ABAC ML pipeline
# For quick simulation, training, and policy update without launching live servers

echo "[1/3] Enriching data..."
python3 scripts/enrich_data.py || { echo "[!] Failed: enrich_data.py"; exit 1; }

echo "[2/3] Training model..."
python3 scripts/train_model.py || { echo "[!] Failed: train_model.py"; exit 1; }

echo "[3/3] Simulating ABAC policy refinement..."
python3 scripts/abac_policy_engine.py || { echo "[!] Failed: abac_policy_engine.py"; exit 1; }

echo "[✔] One-time ABAC simulation complete."
echo "Check:"
echo "  - Enriched CSV → data/access_logs_enriched.csv"
echo "  - Trained model → models/rf_model.pkl"
echo "  - Policy log     → data/abac_policy_log.json"