# scripts/enrich_data.py
import pandas as pd
import random
from datetime import datetime

# Load the synthetic log
df = pd.read_csv("data/Synthetic_ABAC_Log_Data.csv")

# Synthetic enrichment
random.seed(42)
geo_choices = ["US", "RU", "CN", "DE", "IN"]
auth_choices = ["OAuth", "APIKey", "None"]
referrers = ["https://google.com", "https://linkedin.com", None, "https://github.com"]
bot_user_agents = ["curl/7.68.0", "python-requests/2.25.1", "HeadlessChrome"]
human_user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.90 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
]

# Add features
geo = []
auth = []
ref = []
cookie = []
req_count = []
headless = []
ua = []
label = []
timestamps = []

for _ in range(len(df)):
    is_bot = random.random() < 0.5  # 50% bot, 50% human for clarity
    geo.append(random.choice(["RU", "CN"]) if is_bot else random.choice(["US", "DE"]))
    auth.append("None" if is_bot else random.choice(["OAuth", "APIKey"]))
    ref.append(None if is_bot else random.choice(referrers))
    cookie.append(False if is_bot else True)
    req_count.append(random.randint(100, 300) if is_bot else random.randint(1, 15))
    headless.append(True if is_bot else False)
    ua.append(random.choice(bot_user_agents) if is_bot else random.choice(human_user_agents))
    label.append(1 if is_bot else 0)
    timestamps.append(datetime(2025, 5, 12, random.randint(1, 5) if is_bot else random.randint(8, 17), 0).isoformat())

# Add to dataframe
df["geoLocation"] = geo
df["authType"] = auth
df["referrer"] = ref
df["cookieEnabled"] = cookie
df["requestCount"] = req_count
df["headlessDetected"] = headless
df["userAgent"] = ua
df["label"] = label
df["timestamp"] = timestamps

# Save enriched dataset
df.to_csv("data/access_logs_enriched.csv", index=False)
print("[+] Enriched data saved to data/synth_access_logs_enriched.csv")
