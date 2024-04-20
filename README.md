Bandwidth Tracker with Historical Analysis

This Python application is designed to monitor real-time bandwidth usage, generate usage reports over specified periods, and analyze trends in data usage. Utilizing libraries such as psutil for monitoring system network statistics, pandas for data manipulation and analysis, matplotlib for visualization, and numpy for numerical calculations, it offers a comprehensive tool for tracking and understanding bandwidth consumption patterns.
Features

    Real-Time Bandwidth Monitoring: Continuously track the sending and receiving rates of data over your network connection.
    Historical Usage Reports: Generate detailed reports of your bandwidth usage daily, weekly, monthly, yearly, or even hourly for the current day.
    Trend Analysis: Analyze the trend of your data usage over time to identify patterns and potential issues.

Requirements

To run this application, you will need Python 3.6 or later and the following Python libraries:

    psutil
    pandas
    matplotlib
    numpy

Installation

First, ensure you have Python installed on your system. Then, install the required libraries using pip:

bash

pip install -r requirements.txt

Clone this repository or download the script to your local machine.
Usage

The application can be run from the command line. Navigate to the directory containing the script and run one of the following commands based on your needs:
To Monitor Bandwidth Usage:

bash

python main.py --monitor

This command starts monitoring your bandwidth usage, saving the data to a JSON file in real-time.
To Generate Usage Reports:

bash

python main.py --report [period]

Replace [period] with one of the following to generate the respective report: hourly, daily, weekly, monthly, yearly. For hourly reports, only data from the current day will be considered.
To Analyze Bandwidth Usage Trends:

bash

python main.py --analyze

This command generates a trend analysis of your daily bandwidth usage, helping you visualize usage patterns over time.
Contributing

Contributions to this project are welcome. Please feel free to fork the repository, make changes, and submit pull requests.
License

This project is licensed under the MIT License - see the LICENSE file for details.
