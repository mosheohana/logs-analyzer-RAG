"""
Log Analyzer Project

This script loads raw Apache access log data, parses it into structured fields,
and produces basic descriptive statistics and visualizations.
It demonstrates log ingestion, regex-based parsing, dataframe creation,
and simple exploratory analysis.
"""

import pandas as pd
import re
import matplotlib.pyplot as plt

LOG_FILE = "apache_logs.txt"

# ---------------- 1) Load log file ----------------
print("Loading log file...")

with open(LOG_FILE, "r") as f:
    lines = f.readlines()

print(f"Loaded {len(lines)} log lines")

df = pd.DataFrame({"raw": lines})

# ---------------- 2) Parse log lines ----------------
pattern = re.compile(
    r'(?P<ip>\S+) - - \[(?P<time>.*?)\] "(?P<method>\S+) (?P<path>\S+) \S+" (?P<status>\d{3}) (?P<size>\S+)'
)

def parse_line(line):
    match = pattern.match(line)
    if match:
        return match.groupdict()
    return None

parsed = df["raw"].apply(parse_line).dropna()
df_parsed = pd.DataFrame(parsed.tolist())

# ---------------- 3) Type conversions ----------------
df_parsed["time"] = pd.to_datetime(
    df_parsed["time"],
    format="%d/%b/%Y:%H:%M:%S %z",
    errors="coerce"
)

df_parsed["status"] = df_parsed["status"].astype(int)

# ---------------- 4) Output preview and statistics ----------------
print("\nSample parsed rows:")
print(df_parsed.head())

print("\nTop 5 IP addresses:")
print(df_parsed["ip"].value_counts().head(5))

print("\nHTTP status code distribution:")
print(df_parsed["status"].value_counts())

print("\nTop requested paths:")
print(df_parsed["path"].value_counts().head(5))

# ---------------- 5) Save to CSV ----------------
df_parsed.to_csv("parsed_logs.csv", index=False)
print("\nSaved parsed logs to parsed_logs.csv")

# ---------------- 6) Visualizations ----------------

# Top 5 IPs
plt.figure()
df_parsed["ip"].value_counts().head(5).plot(kind="bar")
plt.title("Top 5 IP addresses")
plt.xlabel("IP address")
plt.ylabel("Request count")
plt.tight_layout()
plt.show()

# HTTP status distribution
plt.figure()
df_parsed["status"].value_counts().sort_index().plot(kind="bar")
plt.title("HTTP status code distribution")
plt.xlabel("Status code")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# Requests over time (per hour)
plt.figure()
requests_per_hour = df_parsed.set_index("time").resample("h").size()
requests_per_hour.plot()
plt.title("Requests over time (hourly)")
plt.xlabel("Time")
plt.ylabel("Number of requests")
plt.tight_layout()
plt.show()

print("\nAnalysis complete.")
