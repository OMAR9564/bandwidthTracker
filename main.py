import argparse
import json
import os
import subprocess
from datetime import datetime
import psutil

# Save monitoring data
DATA_FILE = "bandwidth_usage.json"

def monitor_bandwidth(interval=1):
    ## Monitors real time bandwidth usage and save in JSON file.
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)

    old_sent = psutil.net_io_counters().bytes_sent
    old_recv = psutil.net_io_counters().bytes_recv

    while True:
        new_sent = psutil.net_io_counters().bytes_sent
        new_recv = psutil.net_io_counters().bytes_recv
        sent_rate = (new_sent - old_sent) / interval
        recv_rate = (new_recv - old_recv) / interval

        data_point = {
            "timestamp": datetime.now().isoformat(),
            "sent_rate": sent_rate,
            "recv_rate": recv_rate
        }

        with open(DATA_FILE, "r+") as f:
            data = json.load(f)
            data.append(data_point)
            f.seek(0)
            json.dump(data, f, indent=4)

        old_sent, old_recv = new_sent, new_recv
        time.sleep(interval)

def generate_report(period="daily"):
    ## Generate usage report for specified period.
    subprocess.run(["streamlit", "run", "streamlitReport.py", period], check=True)

def analyze_trends():
    subprocess.run(["streamlit", "run", "streamlitAnalyze.py"], check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bandwidth Tracker with Historical Analysis")
    parser.add_argument("--monitor", action="store_true", help="Start monitoring bandwidth usage.")
    parser.add_argument("--report", type=str, choices=["hourly", "daily", "weekly", "monthly", "yearly"], help="Generate bandwidth usage report.")
    parser.add_argument("--analyze", action="store_true", help="Analyze bandwidth usage trends.")

    args = parser.parse_args()

    if args.monitor:
        print("Starting monitoring bandwidth...\n")
        monitor_bandwidth()
    elif args.report:
        print(f"Generating {args.report} bandwidth usage report...\n")
        generate_report(args.report)
    elif args.analyze:
        print("Analyzing bandwidth...\n")
        analyze_trends()
