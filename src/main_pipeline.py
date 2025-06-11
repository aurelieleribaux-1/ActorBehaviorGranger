"""
Main pipeline script for Time Series analysis using Granger.
This script contains:
  - Dataset creation functions
  - Preprocessing steps for behavior analysis
  - Granger causality preparation and calculation
"""

import pandas as pd
import pm4py
import gzip
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from DyLoPro import DynamicLogPlots

XES_NAMESPACE = {'xes': 'http://www.xes-standard.org/'}


def read_xes_with_pm4py(file_path):
    """Read a .xes file using PM4PY."""
    log = pm4py.read_xes(file_path)
    df = pd.DataFrame()
    if log:
        df = pd.DataFrame([dict(event) for trace in log for event in trace])
    return df


def preprocess_behavior_data(df):
    """Standardize column names and calculate waiting times."""
    df.rename(columns={
        "case_id": "case:concept:name",
        "event_i": "concept:name",
        "timestamp_i": "time:timestamp",
        "accepted_i": "accepted",
        "case_outcome": "case_outcome",
        "case_accepted": "case_accepted",
        "case_canceled": "case_canceled",
        "case_refused": "case_refused",
        "tt_days": "TT"
    }, inplace=True)
    df["time:timestamp"] = pd.to_datetime(df["time:timestamp"])
    return df


def analyze_behavior(df, behavior_type, time_unit='days'):
    """Analyze behavior type using DyLoPro and plot."""
    df_behavior = df[df['behavior'] == behavior_type].copy()
    df_behavior['delta_t'] = (
        df_behavior.groupby('case:concept:name')['time:timestamp']
        .diff().dt.total_seconds() / 86400
    ).fillna(0)

    plot_dc = DynamicLogPlots(
        event_log=df_behavior,
        case_id_key="case:concept:name",
        activity_key="concept:name",
        timestamp_key="time:timestamp",
        numerical_eventfeatures=["delta_t"]
    )

    result = plot_dc.num_eventfts_evol(
        numeric_event_list=["delta_t"],
        time_unit=time_unit,
        numEventFt_transform='mean'
    )

    return result


def export_granger_timeseries(df):
    """Prepare time series for Granger causality analysis."""
    behavior_daily = df.groupby([
        df['time:timestamp'].dt.to_period('D').apply(lambda r: r.start_time),
        'behavior'
    ]).size().unstack(fill_value=0)
    top_behaviors = df['behavior'].value_counts().head(4).index.tolist()

    timeseries = []
    for behavior in top_behaviors:
        if behavior in behavior_daily.columns:
            timeseries.append(behavior_daily[behavior].rename(f"All_{behavior}"))

    df_all = pd.concat(timeseries, axis=1).sort_index().fillna(0)
    return df_all


def main():
    """Run the main pipeline example."""
    # Example file
    file_path = "data/BPI_Challenge_2017.xes.gz"
    df_raw = read_xes_with_pm4py(file_path)
    print(df_raw.head())

    # Preprocess data (example)
    df_processed = preprocess_behavior_data(df_raw)
    print(df_processed.columns)

    # Analyze a behavior type (example)
    analyze_behavior(df_processed, behavior_type="C", time_unit='weeks')

    # Prepare timeseries for Granger
    ts = export_granger_timeseries(df_processed)
    print(ts.head())

    # Save example
    ts.to_csv("data/bpic2017_timeseries.csv", index=True)
    print("✅ Exported timeseries for Granger analysis.")


if __name__ == "__main__":
    main()
