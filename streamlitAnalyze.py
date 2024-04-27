import streamlit as st
import pandas as pd
import numpy as np
import json
import altair as alt
from sklearn.linear_model import LinearRegression
import sys

# Veri yükleme fonksiyonu
@st.cache_resource
def load_data():
    with open("bandwidth_usage.json", "r") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['total_usage'] = df['sent_rate'] + df['recv_rate']
    return df

df = load_data()

# Veri setini zaman serisine göre gruplama ve toplama
df_grouped = df.resample('D', on='timestamp').sum()  # 'D' günlük toplam için, 'H' saatlik toplam için kullanılabilir.

# Doğrusal Regresyon Modeli
model = LinearRegression()
df_grouped['day'] = np.arange(len(df_grouped))  # Gün sayısı olarak x eksenini oluşturmak
X = df_grouped[['day']]  # Bağımsız değişken
y = df_grouped['total_usage']  # Bağımlı değişken

model.fit(X, y)
df_grouped['trend'] = model.predict(X)

# Trend grafiğini çizdirme
chart = alt.Chart(df_grouped.reset_index()).mark_line().encode(
    x='timestamp:T',
    y='total_usage:Q',
    tooltip=['timestamp', 'total_usage']
).properties(
    title="Bandwidth Usage Over Time"
)

trend_line = alt.Chart(df_grouped.reset_index()).mark_line(color='red').encode(
    x='timestamp:T',
    y='trend:Q'
)

# Anomali Tespiti için Z-score hesaplama
df_grouped['z_score'] = (df_grouped['total_usage'] - df_grouped['total_usage'].mean()) / df_grouped['total_usage'].std()
threshold = 2  # Genellikle kullanılan bir eşik değer
anomalies = df_grouped[abs(df_grouped['z_score']) > threshold]

# Anomali noktalarını işaretleme
anomaly_points = alt.Chart(anomalies.reset_index()).mark_circle(size=100, color='red').encode(
    x='timestamp:T',
    y='total_usage:Q',
    tooltip=['timestamp', 'total_usage', 'z_score']
)

st.altair_chart(chart + trend_line + anomaly_points, use_container_width=True)
