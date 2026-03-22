import streamlit as st
import pandas as pd
import numpy as np
import csv
import os
import store

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
    #:列3 Region "ap-northeast-1"
    #:列4 CostUSD "2.09"
    #:列5 UsageQuantity "32.25"

    df["Date"] = pd.to_datetime(df["Date"])

    #:日付フィルタ
    if st.checkbox("日付フィルタを有効にする"):
        start_date = st.date_input("開始日", key="start_date")
        finish_date = st.date_input("終了日", key="finish_date")
        query_text = f'"{start_date}" <= Date < "{finish_date}"'
        df = df.query(query_text)

    #:サービスフィルタ
    if st.checkbox("サービスフィルタを有効にする"):
        service_list = df["Service"].unique()
        selected_service_list = st.multiselect(
            label="サービスを選択してください。",
            options=service_list,
            default=service_list,
        )
        df = df.query("Service in @selected_service_list")

    #:月毎の total cost を集計する。
    st.header("月毎の total cost")
    df["Month"] = df["Date"].dt.strftime("%Y-%m")
    monthly = df.groupby("Month")["CostUSD"].sum().reset_index()
    st.dataframe(monthly)
    st.bar_chart(monthly, x="Month", x_label="Month")
    #:expected | 2025-09 | 2987.55 |
    #:actual   | 2025-09 | 2987.55 |

    #:Service別コストを集計する。
    st.header("Service別コスト")
    service_monthly = df.groupby(["Month", "Service"])["CostUSD"].sum().reset_index()
    service_monthly_pivot = service_monthly.pivot(
        index="Month", columns="Service", values="CostUSD"
    )
    st.dataframe(service_monthly_pivot)
    #:         | Month.  | Service  | CostUSD |
    #:expected | 2025-09 | AWS CloudTrail | 160.68 |
    #:actual   | 2025-09 | AWS CloudTrail | 160.68 |
    st.bar_chart(service_monthly_pivot)

    #:Region別コストを集計する。
    st.header("Region別コスト")
    region_monthly = df.groupby(["Month", "Region"])["CostUSD"].sum().reset_index()
    region_monthly_pivot = region_monthly.pivot(
        index="Month", columns="Region", values="CostUSD"
    )
    st.dataframe(region_monthly_pivot)
    st.bar_chart(region_monthly_pivot)
    #:         | Month.  | Region | CostUSD |
    #:expected | 2025-09 | us-west-2 | 995.81 |
    #:actual   | 2025-09 | us-west-2 | 995.81 |
