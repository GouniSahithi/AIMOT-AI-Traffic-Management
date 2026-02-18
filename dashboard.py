import streamlit as st
import json
import time
import pandas as pd
import os

st.set_page_config(page_title="Traffic Simulation Dashboard", layout="wide")
st.markdown("""
    <style>
    .stApp {
        background-color: #0c0c0c;
        color: white;
    }
    .big-title {
        font-size: 36px;
        font-weight: bold;
        color: #ffffff;
    }
    .card {
        background-color: #292b2c;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='big-title'>🚦 Intelligent Traffic Management Dashboard</h1>", unsafe_allow_html=True)

data_file = "simulation_data.json"
REFRESH_INTERVAL = 1  # seconds

placeholder = st.empty()

def render_dashboard(data):
    with placeholder.container():
        # Simulation time
        st.markdown(f"### ⏱️ Simulation Time: `{data['time']}s`")

        # Lane Stats Table
        df = pd.DataFrame(data["lanes"])
        df["emergency"] = df["emergency"].apply(lambda x: "🚨" if x else "")
        df.columns = ["Lane ID", "Direction", "Passed Vehicles", "Waiting", "Emergency"]
        st.dataframe(df, use_container_width=True, height=250)

        # Vehicle Type Breakdown
        if "vehicle_types" in data:
            st.subheader("🚗 Vehicle Type Breakdown")
            vt_df = pd.DataFrame.from_dict(data["vehicle_types"], orient="index", columns=["Count"])
            st.bar_chart(vt_df)

        # Vehicles Passed Chart
        st.subheader("📊 Vehicles Passed per Lane")
        st.bar_chart(data=df, x="Direction", y="Passed Vehicles")

        # Emergency Event Log
        st.subheader("🚨 Emergency Event Log")
        for e in reversed(data.get("events", [])[-5:]):
            st.markdown(f"- {e}")

        # Stop if simulation is complete
        if any("Simulation Complete" in log for log in data.get("events", [])):
            st.success("✅ Simulation completed. Dashboard will no longer update.")
            return False

    return True

while True:
    try:
        if os.path.exists(data_file):
            with open(data_file, "r") as f:
                file_content = f.read().strip()
                if file_content:
                    data = json.loads(file_content)
                    should_continue = render_dashboard(data)
                    if not should_continue:
                        break
        else:
            st.warning("Waiting for simulation data...")
    except Exception as e:
        st.error(f"❌ Error reading simulation data: {e}")

    time.sleep(REFRESH_INTERVAL)
