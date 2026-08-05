import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
st.set_page_config(page_title="📊 Wearable Devices Dashboard", layout="wide")
st.title("📱 Wearable Devices Data Dashboard")

base_dir = Path(__file__).resolve.parent.parent
CSV_PATH = base_dir / "data" / "wearable_devices.csv"

try:
    device_data = pd.read_csv(CSV_PATH)
except FileNotFoundError:
    st.error(f"CSV not found at: {CSV_PATH}")
    st.stop()
device_data['Test_Date'] = pd.to_datetime(device_data['Test_Date'], format='mixed', dayfirst=True, errors='coerce')

str_cols = device_data.select_dtypes(include=['object']).columns
device_data[str_cols] = device_data[str_cols].apply(lambda x: x.str.strip())

numeric_cols = ['Price_USD', 'Battery_Life_Hours', 'Heart_Rate_Accuracy_Percent',
                'Step_Count_Accuracy_Percent', 'Sleep_Tracking_Accuracy_Percent',
                'User_Satisfaction_Rating', 'GPS_Accuracy_Meters', 'Health_Sensors_Count', 'Performance_Score']
device_data[numeric_cols] = device_data[numeric_cols].apply(pd.to_numeric, errors='coerce')

st.subheader("📌 Dataset Preview")
st.dataframe(device_data.head())

with st.sidebar:
    st.header("🔍 Filter Options")
    brand_filter = st.multiselect("Select Brand(s):", device_data["Brand"].dropna().unique())
    category_filter = st.multiselect("Select Category:", device_data["Category"].dropna().unique())

filtered_data = device_data.copy()
if brand_filter:
    filtered_data = filtered_data[filtered_data["Brand"].isin(brand_filter)]
if category_filter:
    filtered_data = filtered_data[filtered_data["Category"].isin(category_filter)]

st.subheader("📉 Filtered Data Preview")
st.dataframe(filtered_data)

# Plot 1: Price vs Performance
st.subheader("💸 Price vs Performance Score")
fig1 = px.scatter(filtered_data, x="Price_USD", y="Performance_Score", color="Brand",
                  hover_data=["Device_Name", "Model"], title="Price vs Performance Score")
st.plotly_chart(fig1, use_container_width=True)

# Plot 2: Battery Life Distribution
st.subheader("🔋 Battery Life Distribution")
fig2 = px.histogram(filtered_data, x="Battery_Life_Hours", color="Brand", nbins=30,
                    title="Battery Life Distribution")
st.plotly_chart(fig2, use_container_width=True)

# Plot 3: Step Count vs Heart Rate Accuracy
st.subheader("❤️ Step vs Heart Rate Accuracy")
fig3 = px.scatter(filtered_data, x="Step_Count_Accuracy_Percent", y="Heart_Rate_Accuracy_Percent",
                  color="Brand", title="Step Count Accuracy vs Heart Rate Accuracy")
st.plotly_chart(fig3, use_container_width=True)

# Plot 4: Sleep Tracking Accuracy by Brand
st.subheader("🛌 Sleep Tracking Accuracy by Brand")
fig4 = px.box(filtered_data, x="Brand", y="Sleep_Tracking_Accuracy_Percent", color="Brand",
              title="Sleep Tracking Accuracy Distribution by Brand")
st.plotly_chart(fig4, use_container_width=True)

# Plot 5: Health Sensors Count vs Performance
st.subheader("📟 Health Sensors Count vs Performance Score")
fig5 = px.scatter(filtered_data, x="Health_Sensors_Count", y="Performance_Score",
                  size="Price_USD", color="Brand", title="Health Sensors vs Performance")
st.plotly_chart(fig5, use_container_width=True)

# Plot 6: Category-wise Avg Performance
st.subheader("📊 Average Performance by Category")
if "Category" in filtered_data.columns:
    category_perf = filtered_data.groupby("Category", as_index=False)["Performance_Score"].mean()
    fig8 = px.bar(category_perf, x="Category", y="Performance_Score", color="Category",
                  title="Average Performance Score by Category")
    st.plotly_chart(fig8, use_container_width=True)
