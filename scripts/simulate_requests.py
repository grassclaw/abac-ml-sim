import random, csv
from datetime import datetime

roles = ["Developer", "Recruiter", "General"]
user_agents = ["Mozilla", "Chrome", "HeadlessChrome", "BotAgent"]
ips = ["192.168.1." + str(i) for i in range(2, 50)]

def generate_request():
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "ip": random.choice(ips),
        "user_role": random.choice(roles),
        "user_agent": random.choice(user_agents),
        "request_rate": random.randint(1, 100),
        "accessed_resource": "linkedin_profile"
    }

with open("data/access_logs.csv", "w", newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(generate_request().keys()))
    writer.writeheader()
    for _ in range(500):
        writer.writerow(generate_request())
