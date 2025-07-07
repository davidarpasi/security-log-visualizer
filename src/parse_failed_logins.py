import re
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt
import os

# Log file path
LOG_FILE = os.path.join("..", "logs", "sample_auth.log")

# Regex pattern (example: Jun 18 07:13:45)
pattern = r'^(?P<month>\w{3}) (?P<day>\d{1,2}) (?P<time>\d{2}:\d{2}):\d{2} .* Failed password .*'

# Parser
def parse_failed_logins(log_path):
    counts = Counter()
    with open(log_path, "r") as f:
        for line in f:
            match = re.match(pattern, line)
            if match:
                timestamp_str = f"2024 {match.group('month')} {match.group('day')} {match.group('time')}"
                try:
                    timestamp = datetime.strptime(timestamp_str, "%Y %b %d %H:%M")
                    hour = timestamp.replace(minute=0)
                    counts[hour] += 1
                except ValueError:
                    continue
    return counts

# Draw graph
def plot_attempts(counts):
    times = sorted(counts.keys())
    values = [counts[t] for t in times]
    plt.figure(figsize=(10, 5))
    plt.plot(times, values, marker="o", color="crimson")
    plt.title("Failed Login Attempts per Hour")
    plt.xlabel("Time")
    plt.ylabel("Failed Attempts")
    plt.xticks(rotation=45)
    plt.tight_layout()
    os.makedirs("../output", exist_ok=True)
    plt.savefig("../output/failed_login_plot.png")
    print("[+] Plot saved to output/failed_login_plot.png")

if __name__ == "__main__":
    print("[*] Parsing log file...")
    data = parse_failed_logins(LOG_FILE)
    plot_attempts(data)
