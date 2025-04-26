import streamlit as st
import pandas as pd
from data_loader import load_data
from processor import process_logs, detect_anomalies, calculate_risk_score
from visualizer import (
    plot_latency_trend, plot_downtime_events, plot_service_heatmap,
    plot_risk_trend, plot_success_rate
)
from utils.logger import setup_logger

logger = setup_logger()
st.set_page_config(page_title="VAS Performance Dashboard", layout="wide")

@st.cache_data
def load_cached(path_or_file):
    try:
        return load_data(path_or_file)
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise

def main():
    st.title("VAS Performance Analysis Dashboard")
    st.markdown("Monitor and analyze the health of Value-Added Services (SMS, USSD, IVR, etc.)")

    st.sidebar.header("Controls")
    service = st.sidebar.selectbox("Select Service", ["All", "SMS", "USSD", "IVR"])
    time_range = st.sidebar.slider("Select Time Range (hours)", 1, 24, 12, help="How many past hours of data to analyze.")

    uploaded_file = st.sidebar.file_uploader("Upload VAS log CSV", type="csv")
    df = None
    if uploaded_file:
        try:
            df = load_cached(uploaded_file)
        except Exception as e:
            st.error(f"Failed to load uploaded file: {str(e)}")
            return
    else:
        try:
            df = load_cached("data/fake_vas_logs.csv")
        except FileNotFoundError:
            st.error("Default data file (data/fake_vas_logs.csv) not found. Please upload a CSV file.")
            return
        except Exception as e:
            st.error(f"Error loading default data: {str(e)}")
            return

    if st.sidebar.checkbox("Auto-refresh every 30s"):
        st.warning("Auto-refresh is disabled in this version. Please refresh manually.")

    try:
        # Validate DataFrame columns
        required_columns = ['timestamp', 'service', 'status', 'latency_ms']
        if not all(col in df.columns for col in required_columns):
            st.error(f"CSV must contain columns: {required_columns}")
            return

        processed_df = process_logs(df, service, time_range)
        anomalies = detect_anomalies(processed_df)
        risk_scores = calculate_risk_score(processed_df)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Latency Trend")
            st.plotly_chart(plot_latency_trend(processed_df), use_container_width=True)

            st.subheader("Downtime Events")
            st.plotly_chart(plot_downtime_events(processed_df), use_container_width=True)

        with col2:
            st.subheader("Service Latency Heatmap")
            st.plotly_chart(plot_service_heatmap(processed_df), use_container_width=True)

            st.subheader("Success Rate")
            st.plotly_chart(plot_success_rate(processed_df), use_container_width=True)

        st.subheader("Risk Score Trend")
        st.plotly_chart(plot_risk_trend(risk_scores), use_container_width=True)

        st.subheader("Detected Anomalies")
        if not anomalies.empty:
            st.dataframe(anomalies[["timestamp", "service", "latency_ms", "anomaly_score"]])
            st.download_button("Download Anomalies", anomalies.to_csv(index=False), "anomalies.csv")
        else:
            st.write("No anomalies detected.")

    except Exception as e:
        logger.error(f"Error in dashboard: {str(e)}")
        st.error(f"An error occurred while loading the dashboard: {str(e)}")

if __name__ == "__main__":
    main()
