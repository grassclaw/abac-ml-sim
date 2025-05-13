# scripts/abac_cli_test.py
import requests
import json
import os
from datetime import datetime

LOG_PATH = "data/live_requests.json"

# Load or initialize log
if os.path.exists(LOG_PATH):
    with open(LOG_PATH, "r") as f:
        request_log = json.load(f)
else:
    request_log = []

print("🔐 ABAC Live Check CLI + Logging\n")

example = {
    "requestCount": 250,
    "cookieEnabled": False,
    "headlessDetected": True
}

while True:
    print("\nEnter values for the request or press Enter to use defaults:")
    try:
        req_count = input(f"Request Count [{example['requestCount']}]: ") or example['requestCount']
        cookie = input(f"Cookie Enabled (0/1) [{int(example['cookieEnabled'])}]: ") or int(example['cookieEnabled'])
        headless = input(f"Headless Detected (0/1) [{int(example['headlessDetected'])}]: ") or int(example['headlessDetected'])

        payload = {
            "requestCount": int(req_count),
            "cookieEnabled": int(cookie),
            "headlessDetected": int(headless)
        }

        r = requests.post("http://localhost:5001/abac_check", json=payload)
        result = r.json()

        print("\n[Response]", json.dumps(result, indent=2))

        # Log with timestamp
        result_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "input": payload,
            "decision": result.get("decision", "UNKNOWN")
        }
        request_log.append(result_entry)

        with open(LOG_PATH, "w") as f:
            json.dump(request_log, f, indent=2)

    except KeyboardInterrupt:
        print("\n[+] Exiting CLI test...")
        break
    except Exception as e:
        print("[!] Error:", e)
