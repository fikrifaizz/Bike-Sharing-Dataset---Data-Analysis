import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# Convert date column
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Mapping season numbers to names
season_mapping = {1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"}
day_df['season_name'] = day_df['season'].map(season_mapping)

# Sidebar filters
st.sidebar.header("Filter Data")
st.sidebar.subheader("Filter Data berdasarkan Tanggal")
start_date = pd.to_datetime(st.sidebar.date_input("Pilih tanggal awal", day_df['dteday'].min()))
end_date = pd.to_datetime(st.sidebar.date_input("Pilih tanggal akhir", day_df['dteday'].max()))
season_filter = st.sidebar.multiselect("Pilih Musim", options=list(season_mapping.values()), default=list(season_mapping.values()))

# Apply filters
day_filtered = day_df[(day_df['dteday'] >= start_date) & (day_df['dteday'] <= end_date) & (day_df['season_name'].isin(season_filter))]
hour_filtered = hour_df[(hour_df['dteday'] >= start_date) & (hour_df['dteday'] <= end_date)]

# Title
st.title("Dashboard Bike Sharing")

# 1. Pengaruh Hari Libur terhadap Pengguna Sepeda
st.subheader("Pengaruh Hari Libur terhadap Jumlah Pengguna Sepeda")
holiday_counts = day_filtered.groupby("holiday")[["cnt"]].mean()
fig, ax = plt.subplots()
ax.bar(['Hari Biasa', 'Hari Libur'], holiday_counts["cnt"], color=['blue', 'red'])
ax.set_ylabel("Rata-rata Jumlah Pengguna")
ax.set_title(f"Hari Biasa: {int(holiday_counts.iloc[0][0])} | Hari Libur: {int(holiday_counts.iloc[1][0])}")
st.pyplot(fig)

# 2. Distribusi Pengguna pada Jam Sibuk
st.subheader("Distribusi Pengguna Sepeda selama Jam Sibuk")
peak_hours = hour_filtered[(hour_filtered['hr'].between(7, 9)) | (hour_filtered['hr'].between(17, 19))]
fig, ax = plt.subplots(figsize=(8, 4))
sns.boxplot(x=peak_hours['hr'], y=peak_hours['cnt'], ax=ax)
ax.set_xlabel("Jam")
ax.set_ylabel("Jumlah Pengguna")
ax.set_title(f"Rata-rata Pengguna Jam Sibuk: {int(peak_hours['cnt'].mean())}")
st.pyplot(fig)

# 3. Pengaruh Cuaca terhadap Penggunaan Sepeda
st.subheader("Pengaruh Cuaca terhadap Penggunaan Sepeda")
weather_counts = day_filtered.groupby("weathersit")["cnt"].mean()
fig, ax = plt.subplots()
ax.bar(['Cerah', 'Berawan', 'Hujan'], weather_counts, color=['green', 'orange', 'gray'])
ax.set_ylabel("Rata-rata Jumlah Pengguna")
ax.set_title(f"Cerah: {int(weather_counts.iloc[0])} | Berawan: {int(weather_counts.iloc[1])} | Hujan: {int(weather_counts.iloc[2])}")
st.pyplot(fig)

# 4. Perbandingan Penggunaan Sepeda di Berbagai Musim
st.subheader("Perbandingan Penggunaan Sepeda di Berbagai Musim")
season_counts = day_filtered.groupby("season_name")["cnt"].mean()
fig, ax = plt.subplots()
ax.bar(season_counts.index, season_counts, color=['yellow', 'red', 'brown', 'blue'])
ax.set_ylabel("Rata-rata Jumlah Pengguna")
ax.set_title(" | ".join([f"{season}: {int(count)}" for season, count in zip(season_counts.index, season_counts)]))
st.pyplot(fig)

# 5. Tren Penggunaan Sepeda dari 2011 ke 2012
st.subheader("Tren Penggunaan Sepeda dari 2011 ke 2012")
fig, ax = plt.subplots()
filtered_trend = day_filtered.groupby('dteday')['cnt'].sum()
ax.plot(filtered_trend.index, filtered_trend.values, color='purple')
ax.set_ylabel("Jumlah Pengguna Harian")
ax.set_xlabel("Tanggal")
ax.set_title(f"Rata-rata Pengguna Harian: {int(filtered_trend.mean())}")
st.pyplot(fig)

st.write("\n**Catatan:** Data diambil dari Bike Sharing Dataset dan telah difilter sesuai pilihan pengguna.")
