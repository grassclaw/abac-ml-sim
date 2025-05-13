# abac-ml-sim
# ML-Driven ABAC Proof of Concept

This project simulates bot scraping and tests a machine-learning-driven Attribute-Based Access Control (ABAC) system.

## How to Run

### Build Docker
```bash
docker build -t abac-ml-sim .
```

abac-ml-sim/
├── data/
│   ├── access_logs.csv          # Simulated request logs
│   └── abac_policy.json         # Placeholder for simple policy settings
├── models/
│   └── rf_model.pkl             # Trained ML model
├── scripts/
│   ├── simulate_requests.py     # Simulates access events (normal + scraping)
│   ├── train_model.py           # Trains the anomaly detection model
│   ├── abac_policy_engine.py    # Enforces ABAC decisions using the model
│   └── run_all.sh               # Script to run the full pipeline
├── Dockerfile                   # Container definition
├── docker-compose.yml          # (Optional) Compose service definition
├── .gitignore                  # Ignore models/, pycache/, etc.
└── README.md                   # Documentation and instructions
