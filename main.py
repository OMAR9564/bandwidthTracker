import argparse
import json
import os
import time
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import psutil

#Save monitoring data
DATA_FILE = "bandwidth_usage.json"

file_name = os.path.basename(__file__)

def monitor_bandwidth(interval=1):

    ## Monitors real time bandwidth usage and save in JSON file.

    # Control if DATA_FILE is already exist
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)

    old_sent = psutil.net_io_counters().bytes_sent
    old_recv = psutil.net_io_counters().bytes_recv

    while True:
        new_sent = psutil.net_io_counters().bytes_sent
        new_recv = psutil.net_io_counters().bytes_recv

        # calculate send's and recv's speed (byte/sec)
        sent_rate = (new_sent - old_sent) / interval
        recv_rate = (new_recv - old_recv) / interval

        # ready to save data in json
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

    ##Generate usage report for specified period.

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)

    if period == "daily":
        df = df.resample('D').sum()
    elif period == "weekly":
        df = df.resample('W').sum()
    elif period == "monthly":
        df = df.resample('M').sum()
    elif period == "yearly":
        df = df.resample('A').sum()
    elif period == "hourly":
        today = datetime.now().date()
        df = df[df.index.date == today]
        df = df.resample('h').sum()

    df['total_usage'] = df['sent_rate'] + df['recv_rate']

    if period == "hourly":
        df.plot(kind='bar', y='total_usage', title='Today\'s Hourly Bandwidth Usage')
        plt.ylabel('Total Usage (bytes)')
        plt.xlabel('Hour of Day')
        plt.xticks(rotation=45)
    else:
        df.plot(kind='bar', y='total_usage')
        plt.ylabel('Total Usage (bytes)')
        plt.title(f'{period.capitalize()} Bandwidth Usage')
    plt.show()

def analyze_trends():

    ## Analayis data usage trend.

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    # convert data from DataFrame
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)

    daily_usage = df.resample('D').sum()
    daily_usage['total_usage'] = daily_usage['sent_rate'] + daily_usage['recv_rate']

    trend = np.polyfit(range(len(daily_usage.index)), daily_usage['total_usage'], 1)
    trend_poly = np.poly1d(trend)

    plt.plot(daily_usage.index, daily_usage['total_usage'], label='Daily Usage')
    plt.plot(daily_usage.index, trend_poly(range(len(daily_usage.index))), label='Trend', color='red')
    plt.ylabel('Total Usage (bytes)')
    plt.title('Bandwidth Usage Trend')
    plt.legend()
    plt.show()

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
        print("Generating bandwidth usage report...\n")
        generate_report(args.report)
    elif args.analyze:
        print("Analyzing bandwidth...\n")
        analyze_trends()
    else:
        print("Bandwidth Tracker with Historical Analysis\n")
        print("Warning usage this app!!\nPlease read the following.")

        print(f"Operators:\n\t"
              f"To Monitor Bandwidth: python {file_name} --monitor\n\t"
              f"To Generate Report: python {file_name} --report (hourly, daily, weekly, monthly, yearly) \n\t"
              f"To Analyze: python {file_name} --analyze\n")

