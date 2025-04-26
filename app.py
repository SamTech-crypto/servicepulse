import streamlit as st
import pandas as pd
from analysis.data_loader import load_data
from analysis.processor import process_logs, detect_anomalies, calculate_risk_score
from analysis.visualizer import (
    plot_latency_trend, plot_downtime_events, plot_service_heatmap,
    plot_risk_trend, plot_success_rate
)
from utils.logger import setup_logger

logger = setup_logger()
st.set_page_config(page_title="VAS Performance Dashboard", layout="wide")

@st.cache_data
def load_cached(path_or_file):
    return load_data(path_or_file)

def main():
    st.title("VAS Performance Analysis Dashboard")
    st.markdown("Monitor and analyze the health of Value-Added Services (SMS, USSD, IVR, etc.)")

    st.sidebar.header("Controls")
    service = st.sidebar.selectbox("Select Service", ["All", "SMS", "USSD", "IVR"])
    time_range = st.sidebar.slider("Select Time Range (hours)", 1, 24, 12, help="How many past hours of data to analyze.")

    uploaded_file = st.sidebar.file_uploader("Upload VAS log CSV", type="csv")
    if uploaded_file:
        df = load_cached(uploaded_file)
    else:
        df = load_cached("data/fake_vas_logs.csv")

    if st.sidebar.checkbox("Auto-refresh every 30s"):
        st.experimental_rerun()

    try:
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
        st.error("An error occurred while loading the dashboard. Please check logs.")

if __name__ == "__main__":
    main()
