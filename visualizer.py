import plotly.express as px
import pandas as pd
from utils.logger import setup_logger

def plot_latency_trend(df):
    logger = setup_logger()
    try:
        fig = px.line(df, x='timestamp', y='latency_ms', color='service',
                      title="Latency Trend Over Time")
        fig.update_layout(xaxis_title="Time", yaxis_title="Latency (ms)")
        return fig
    except Exception as e:
        logger.error(f"Error plotting latency trend: {str(e)}")
        raise

def plot_downtime_events(df):
    logger = setup_logger()
    try:
        downtime_df = df[df['status'] == 'failed']
        fig = px.scatter(downtime_df, x='timestamp', y='service',
                         title="Downtime Events", color='service')
        fig.update_layout(xaxis_title="Time", yaxis_title="Service")
        return fig
    except Exception as e:
        logger.error(f"Error plotting downtime events: {str(e)}")
        raise

def plot_service_heatmap(df):
    logger = setup_logger()
    try:
        if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        heatmap_data = df.groupby(['service', 'hour'])['latency_ms'].mean().reset_index()
        fig = px.density_heatmap(heatmap_data, x='hour', y='service', z='latency_ms',
                                 title="Latency Heatmap by Service and Hour")
        fig.update_layout(xaxis_title="Hour of Day", yaxis_title="Service")
        return fig
    except Exception as e:
        logger.error(f"Error plotting service heatmap: {str(e)}")
        raise

def plot_risk_trend(risk_df):
    logger = setup_logger()
    try:
        fig = px.line(risk_df, x='timestamp', y='risk_score',
                      title="Risk Score Trend")
        fig.update_layout(xaxis_title="Time", yaxis_title="Risk Score (0-100)")
        return fig
    except Exception as e:
        logger.error(f"Error plotting risk trend: {str(e)}")
        raise

def plot_success_rate(df):
    logger = setup_logger()
    try:
        success_rate = df.groupby('service').apply(
            lambda x: (x['status'] == 'success').mean() * 100
        ).reset_index(name='success_rate')
        fig = px.bar(success_rate, x='service', y='success_rate',
                     title="Success Rate by Service")
        fig.update_layout(xaxis_title="Service", yaxis_title="Success Rate (%)")
        return fig
    except Exception as e:
        logger.error(f"Error plotting success rate: {str(e)}")
        raise
