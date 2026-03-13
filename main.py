import streamlit as st
import pandas as pd
import numpy as np

st.title("はじめてのStreamlit")
st.write("これは簡単なデータ表示アプリです。")

df = pd.DataFrame({
    "x": np.arange(1, 11),
    "y": np.random.randint(10, 100, 10)
})

st.write("サンプルデータ：")
st.dataframe(df)

st.line_chart(df.set_index("x"))
