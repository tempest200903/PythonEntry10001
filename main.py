import streamlit as st
import pandas as pd
import numpy as np
import csv
import os

st.title("クラウドコストダッシュボード")

csv_file_path = "input.csv"
file = st.file_uploader("CSVファイルをアップロードしてください.", type=["csv"])

if file:
    st.text("CSVファイルアップロード成功")
    with open(csv_file_path, "wb") as f:
        f.write(file.read())

if os.path.exists(csv_file_path):
    df = pd.read_csv(csv_file_path)
    st.dataframe(df)
    #:列1 Date "2025-09-13"
    #:列2 Service "Amazon EC2"
    #:列3 CostUSD "2.09"
    #:列4 UsageQuantity "32.25"

    #:月毎の total cost を集計する。
    st.header("月毎の total cost")
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.strftime("%Y-%m")
    monthly = df.groupby("Month")["CostUSD"].sum().reset_index()
    st.dataframe(monthly)
    #:expected | 2025-09 | 2987.55 |
    #:actual   | 2025-09 | 2987.55 |
    st.bar_chart(monthly, x="Month", x_label="Month")

    #:service別コストを集計する。
    st.header("service別コスト")
    service_monthly = df.groupby(["Month", "Service"])["CostUSD"].sum().reset_index()
    chart_data = service_monthly.pivot(
        index="Month", columns="Service", values="CostUSD"
    )
    st.dataframe(chart_data)
    #:         | Month.  | Service  | CostUSD |
    #:expected | 2025-09 | AWS CloudTrail | 160.68 |
    #:actual   | 2025-09 | AWS CloudTrail | 160.68 |
    st.bar_chart(chart_data)
