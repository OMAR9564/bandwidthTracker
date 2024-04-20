# Bandwidth Tracker with Historical Analysis

The Python application tracks real-time bandwidth usage, produces usage reports over time, and determines patterns in data usage. It employs a variety of libraries, including psutil for system network statistics, pandas for data manipulation and analysis, matplotlib for visualization, and numpy for numeric calculations. This application is a one-stop-shop for keeping up with bandwidth usage trends.
## Features
- Real-Time Bandwidth Monitoring: Keep constant track of the data in your network connection being sent and received daily.
- Historical Usage Reports: Create precise and accurate historical reports on the daily, weekly, monthly, yearly, and even hourly basis of the running day.
- Trend Analysis: Get to know the nature of your data usage state by analyzing how it varies daily.
## Requirements

You will need Python 3.6 or later and the following Python libraries:
```
psutil
pandas
matplotlib
numpy
```

## Installation
```
pip install -r requirements.txt
```
Clone this repository or download the script to your machine.
## Usage

### The application can be run from the command line. Go to the directory where the script is located and execute one of the following commands according to your purpose:
**To Monitor Bandwidth Usage:**
```
python main.py --monitor
```
This command starts monitoring your bandwidth usage, saving the data to a JSON file in real-time.

**To Generate Usage Reports:**
```
python main.py --report [period]
```
Replace ```[period]``` with one of the following to access the respective report: ```hourly```, ```daily```, ```weekly```, ```monthly```, ```yearly```. In case of hourly reports, only the data on the current day will be analyzed.

**To Analyze Bandwidth Usage Trends:**
```
python main.py --analyze 
```
This command generates a trend analysis of your daily bandwidth usage by default.
