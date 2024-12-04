import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

def get_total_count_by_hour_df(hour_df):
  hour_count_df =  hour_df.groupby(by="hours").agg({"count_cr": ["sum"]})
  return hour_count_df

def count_by_day_df(day_df):
    day_df_count_2011 = day_df.query(str('dteday >= "2011-01-01" and dteday < "2012-12-31"'))
    return day_df_count_2011

def count_by_holiday_df (day_df):
    holiday_counts_df = day_df.groupby(by=["category_days","year"]).agg({
    "count_cr": "sum"
    }).reset_index()
    return holiday_counts_df

def total_registered_df(day_df):
   reg_df =  day_df.groupby(by="dteday").agg({
      "registered": "sum"
    })
   reg_df = reg_df.reset_index()
   reg_df.rename(columns={
        "registered": "register_sum"
    }, inplace=True)
   return reg_df

def total_casual_df(day_df):
   cas_df =  day_df.groupby(by="dteday").agg({
      "casual": ["sum"]
    })
   cas_df = cas_df.reset_index()
   cas_df.rename(columns={
        "casual": "casual_sum"
    }, inplace=True)
   return cas_df

def sum_order (hour_df):
    sum_order_items_df = hour_df.groupby("hours").count_cr.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def macem_season (day_df): 
    season_df = day_df.groupby(by="season").count_cr.sum().reset_index() 
    return season_df

def count_by_monthly_df (day_df):
    monthly_counts_df = day_df.groupby(by=["month","year"]).agg({
    "count_cr": "sum"
}).reset_index()
    return monthly_counts_df


days_df = pd.read_csv("dashboard/all_data.csv")
hours_df = pd.read_csv("dashboard/hour_clean.csv")

datetime_columns = ["dteday"]
days_df.sort_values(by="dteday", inplace=True)
days_df.reset_index(inplace=True)   

hours_df.sort_values(by="dteday", inplace=True)
hours_df.reset_index(inplace=True)

for column in datetime_columns:
    days_df[column] = pd.to_datetime(days_df[column])
    hours_df[column] = pd.to_datetime(hours_df[column])

min_date_days = days_df["dteday"].min()
max_date_days = days_df["dteday"].max()

min_date_hour = hours_df["dteday"].min()
max_date_hour = hours_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo/icon
    st.image("dashboard/bike sharing icon.jpg")

        # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])
  
main_df_days = days_df[(days_df["dteday"] >= str(start_date)) & 
                       (days_df["dteday"] <= str(end_date))]

main_df_hour = hours_df[(hours_df["dteday"] >= str(start_date)) & 
                        (hours_df["dteday"] <= str(end_date))]

hour_count_df = get_total_count_by_hour_df(main_df_hour)
day_df_count_2011 = count_by_day_df(main_df_days)
holiday_counts_df = count_by_holiday_df(main_df_days)
reg_df = total_registered_df(main_df_days)
cas_df = total_casual_df(main_df_days)
sum_order_items_df = sum_order(main_df_hour)
season_df = macem_season(main_df_hour)
monthly_counts_df = count_by_monthly_df (main_df_days)

# Melengkapi Dashboard dengan Berbagai Visualisasi Data
st.header('Bike Sharing Dashboard🚵 ')

st.subheader('Daily Sharing')
col1, col2, col3 = st.columns(3)
 
with col1:
    total_orders = day_df_count_2011.count_cr.sum()
    st.metric("Total Sharing Bike", value=total_orders)

with col2:
    total_sum = reg_df.register_sum.sum()
    st.metric("Total Registered", value=total_sum)

with col3:
    total_sum = cas_df.casual_sum.sum()
    st.metric("Total Casual", value=total_sum)

# Grafik Penyewaan Sepeda Terbanyak dan Sedikit Berdasarkan Jam
st.subheader("Pada jam berapa penyewaan sepeda terbanyak dan sedikit terjadi?")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(22, 8))
colors = ["#D3D3D3", "#D3D3D3", "#0A97B0", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="hours", y="count_cr", data=sum_order_items_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Hours (PM)", fontsize=15)
ax[0].set_title("Jam dengan banyak penyewa sepeda", loc="center", fontsize=15)
ax[0].tick_params(axis='y', labelsize=15)
ax[0].tick_params(axis='x', labelsize=15)

sns.barplot(x="hours", y="count_cr", data=sum_order_items_df.sort_values(by="hours", ascending=True).head(5), palette=["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3","#FF8C9E"], ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Hours (AM)",  fontsize=15)
ax[1].set_title("Jam dengan sedikit penyewa sepeda", loc="center", fontsize=15)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='y', labelsize=15)
ax[1].tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# Grafik Penyewaan Sepeda Tertinggi dan Terendah Berdasarkan Musim
st.subheader("Pada musim apa yang memiliki tingkat penyewaan sepeda tertinggi dan terendah?")

colors = [ "#D3D3D3", "#D3D3D3", "#FF8C9E", "#0A97B0"]
fig, ax = plt.subplots(figsize=(12, 6))

sns.barplot(data=season_df.sort_values(by="season", ascending=False), y="count_cr",x="season", palette=colors,ax=ax)
ax.set_title("Grafik Antar Musim", loc="center", fontsize=15)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)


# Grafik Penyewaan Sepeda Berdasarkan Weekend dan Weekday
st.subheader("Seberapa signifikan jumlah penyewaan sepeda pada saat libur dibanding dengan hari biasa ?")

colors = [ "#FF8C9E", "#0A97B0"]
fig, ax = plt.subplots(figsize=(12, 6))

sns.barplot(data=holiday_counts_df, x="category_days", y="count_cr", hue="year", palette=colors)
plt.ylabel("Jumlah")
plt.title("Jumlah total sepeda yang disewakan berdasarkan hari libur")
plt.legend(title="Tahun", loc="upper right")
plt.tight_layout()
st.pyplot(fig)


# Grafik Penyewaan Sepeda Berdasarkan Customer yang Registered dengan Casual
st.subheader("Perbandingan Customer yang Registered dengan casual")
sizes = [18.8, 81.2]
explode = (0, 0.1) 
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, autopct='%1.1f%%',colors=["#D3D3D3", "#0A97B0"],
        shadow=True, startangle=90)
ax1.axis('equal')  
st.pyplot(fig1)

# Grafik Performa Jumlah penyewaan Sepeda pada Tahun Pertama dibandingkan Tahun Kedua
st.subheader("Bagaimana performa total jumlah penyewaan sepeda pada tahun pertama dibandingkan tahun kedua?")
fig, ax = plt.subplots()
colors = [ "#FF8C9E", "#0A97B0"]

sns.lineplot(data=monthly_counts_df, x="month", y="count_cr", hue="year", palette=colors, marker="o")
plt.xlabel("Nama Bulan")
plt.ylabel("Jumlah")
plt.title("Jumlah total sepeda yang disewakan berdasarkan Bulan dan tahun")
plt.legend(title="Tahun", loc="lower right")  
plt.xticks(ticks=monthly_counts_df["month"], labels=monthly_counts_df["month"])
plt.tight_layout()
for line in ax.lines:
    for x, y in zip(line.get_xdata(), line.get_ydata()):
        plt.text(x, y, '{:.0f}'.format(y), color="white", ha="center", fontsize=8).set_backgroundcolor("gray")
st.pyplot(fig)

st.caption('Copyright © Elsanovita 2024')