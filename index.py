import streamlit as st
import pandas as pd
import numpy as np
import requests
import time

st.set_page_config(
    page_title="Real-Time IoT",
    page_icon="✅",
    layout="wide",
)

st.title("Iot Data")

DATA_URL = 'https://trace.vfsc.vn/iot/xxx'

# def stream():
#     s = requests.Session()
#     with requests.get(DATA_URL, headers=None, stream=True, params={"items":160}) as response:
#         # print(response.status_code)
#         for line in response.iter_lines():
#             if line: print(line)
#             #     print(line.decode('utf-8')['data'])

# stream()


def load_data(n):
    print(n)
    response = requests.get(DATA_URL, params = {"items": n})

    plan = response.json()['plan'] 
    data = response.json()['data']

    return data

df = pd.DataFrame.from_dict(load_data(1))
df.rename({'Lat' : 'LAT', 'Lng' : 'LON'}, axis='columns', inplace=True)


if "count" not in st.session_state:
    st.session_state['count'] = 1


col1, col2 = st.columns(2)

graph_type = "Bar"
data_col   = "STemp"


with col1:
    data_col = st.selectbox(
        "Choose column to plot",
        [col for col in df.columns if col.lower() in "upt, batv, solv, stemp, moment".split(", ")],
    )

    # st.checkbox("Disable selectbox widget", key="disabled")
    graph_type = st.radio(
        "Choose graph type 👉",
        ('Bar', 'Line'),
    )

with col2:
    placeholder = st.empty()
    while True:
        df = pd.DataFrame.from_dict(load_data(st.session_state["count"]))
        df.rename({'Lat' : 'LAT', 'Lng' : 'LON'}, axis='columns', inplace=True)
        with placeholder.container():
            st.map(df)
            if graph_type == 'Line':
                st.line_chart(df[data_col])
            elif graph_type == 'Bar':
                st.bar_chart(df[data_col])
            time.sleep(3)
        st.session_state["count"] += 1


