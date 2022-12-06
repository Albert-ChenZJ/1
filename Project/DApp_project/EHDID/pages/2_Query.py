import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import random
import json
import requests
from PIL import Image
import numpy as np
import base64
from hashlib import sha256
from chain_operation import Eth_Query,Eth_Invoke,Fabric_Invoke,Fabric_Query,Eth_to_Fabric,Fabric_to_Eth

st.set_page_config(layout = "wide")

st.markdown('## Query')
with st.container():
    c1,c2 = st.columns([1,4])
    with c1:
        query_chain = st.radio('Query Chain',['Ethereum','Fabric'])
    with c2:
        query_ID = st.text_input('ID',placeholder='ID on ' + query_chain)
    query_button = st.button('Query')
    if query_button:
        if query_chain == 'Ethereum':
            res = Eth_Query(query_ID) # res type String
            value = json.loads(res)
            
        if query_chain == 'Fabric':
            value = Fabric_Query(query_ID)
            value = json.loads(value)
        with st.container():
            record = {}
            record[query_ID] = {'Face Embedding':value['Face Embedding'],'Hash':value['Hash']}
            df = pd.DataFrame(record)
            st.dataframe(df.transpose(),use_container_width=True)
        # display record
        pass