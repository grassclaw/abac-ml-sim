#!/bin/bash

# stop_all.sh
# Gracefully stops Flask and Streamlit processes launched by run_all.sh

echo "[!] Stopping ABAC environment..."

# Find and kill Flask (live_abac_checker)
FLASK_PID=$(lsof -i :5001 -t)
if [ ! -z "$FLASK_PID" ]; then
  echo "[-] Killing Flask (PID $FLASK_PID)"
  kill $FLASK_PID
else
  echo "[ ] Flask not running on port 5001"
fi

# Find and kill Streamlit (dashboard)
STREAMLIT_PID=$(lsof -i :8501 -t)
if [ ! -z "$STREAMLIT_PID" ]; then
  echo "[-] Killing Streamlit (PID $STREAMLIT_PID)"
  kill $STREAMLIT_PID
else
  echo "[ ] Streamlit not running on port 8501"
fi

echo "[✔] All background processes terminated."
