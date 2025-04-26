import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from utils.logger import setup_logger
from config import LATENCY_THRESHOLD, ERROR_RATE_THRESHOLD

def process_logs(df, service, time_range):
    logger = setup_logger()
    try:
        df['status'] = df['status'].str.lower()  # Normalize
        if service != "All":
            df = df[df['service'] == service]
        end_time = df['timestamp'].max()
        start_time = end_time - pd.Timedelta(hours=time_range)
        df = df[(df['timestamp'] >= start_time) & (df['timestamp'] <= end_time)]
        df = df.fillna({'latency_ms': df['latency_ms'].mean(), 'status': 'unknown'})
        logger.info(f"Processed {len(df)} log entries for {service}")
        return df
    except Exception as e:
        logger.error(f"Error processing logs: {str(e)}")
        raise

def detect_anomalies(df):
    logger = setup_logger()
    try:
        if df.empty:
            return pd.DataFrame()
        X = df[['latency_ms']].values
        model = IsolationForest(contamination=0.1, random_state=42)
        model.fit(X)
        df['anomaly_score'] = model.decision_function(X)
        df['is_anomaly'] = model.predict(X)
        anomalies = df[df['is_anomaly'] == -1]
        logger.info(f"Detected {len(anomalies)} anomalies")
        return anomalies
    except Exception as e:
        logger.error(f"Error detecting anomalies: {str(e)}")
        raise

def calculate_risk_score(df):
    logger = setup_logger()
    try:
        risk_scores = []
        time_groups = df.groupby(pd.Grouper(key='timestamp', freq='1H'))
        for time, group in time_groups:
            latency_score = np.mean(group['latency_ms'] > LATENCY_THRESHOLD) * 0.4
            error_rate = 1 - (group['status'] == 'success').mean()
            error_score = error_rate * 0.4
            downtime_score = (group['status'] == 'failed').mean() * 0.2
            total_score = latency_score + error_score + downtime_score
            risk_scores.append({
                'timestamp': time,
                'risk_score': min(total_score * 100, 100)
            })
        risk_df = pd.DataFrame(risk_scores)
        logger.info("Calculated risk scores")
        return risk_df
    except Exception as e:
        logger.error(f"Error calculating risk score: {str(e)}")
        raise
