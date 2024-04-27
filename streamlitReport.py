import streamlit as st
import pandas as pd
from datetime import datetime
import json
import altair as alt
from streamlit_autorefresh import st_autorefresh
import sys

# Otomatik yenileme için süre belirleyin (örneğin, 1000 ms = 1 saniye)
st_autorefresh(interval=1000, key="data_refresh")

# Veri dosyasının yolu
DATA_FILE = "bandwidth_usage.json"

def convert_bytes(df, column_name):
    """Belirtilen sütundaki byte değerlerini megabyte'a veya gigabyte'a çevirir."""
    df[f"{column_name}_MB"] = df[column_name] / (1024**2)
    df[f"{column_name}_GB"] = df[column_name] / (1024**3)
    return df

def load_data():
    """Veriyi yükler ve işler."""
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)  # UTC olarak belirt
    convert_bytes(df, 'sent_rate')
    convert_bytes(df, 'recv_rate')
    df['total_usage'] = df['sent_rate'] + df['recv_rate']
    convert_bytes(df, 'total_usage')
    return df.set_index('timestamp')

df = load_data()

# Terminalden gelen periyodu oku
if len(sys.argv) > 1:
    period = sys.argv[1]
else:
    period = "daily"

# Altair grafiği için veri hazırlığı
if period == "hourly":
    today = datetime.now().date()
    df = df[df.index.date == today]
    df = df.resample('h').sum()
    title = 'Hourly Usage (GB)'
elif period in ["daily", "weekly", "monthly", "yearly"]:
    df = df.resample(period[0].upper()).sum()
    title = f'{period.capitalize()} Usage (GB)'

df = df[df['total_usage_GB'] > 0]
y_unit = 'total_usage_GB'

# Altair çubuk grafiğini oluştur
chart = alt.Chart(df.reset_index()).mark_bar().encode(
    x=alt.X('timestamp:T', axis=alt.Axis(title='Date')),
    y=alt.Y(f'{y_unit}:Q', axis=alt.Axis(title='Usage (GB)')),
    tooltip=['timestamp:T', f'{y_unit}:Q']
).properties(
    title=title,
    width=800,
    height=400
)

st.altair_chart(chart, use_container_width=True)
