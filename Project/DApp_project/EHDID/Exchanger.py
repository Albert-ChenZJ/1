import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import random
import json
import requests
from chain_operation import Eth_Query,Eth_Invoke,Fabric_Invoke,Fabric_Query,Eth_to_Fabric,Fabric_to_Eth
# import web3

st.set_page_config(layout = "wide")

st.markdown('## Log Identity')
with st.container():
    col1,col2 = st.columns([1,4])
    with col1:
        chain = st.radio('Chain',['Ethereum','Fabric'])
    with col2:
        ID = st.text_input('ID',placeholder=chain)
            
with st.container():
    c1,c2,c3= st.columns(3)
    with c1:
        name = st.text_input('Name')
        birth_date = st.date_input('Date of Birth')
        birth_date = datetime.strftime(birth_date,"%Y/%m/%d")
    with c2:
        address = st.text_input('Address')
        gender = st.selectbox('Gender',['Male','Female'])
    button_log_label = 'Log on ' + chain
    button_log = st.button(button_log_label)
    if button_log:
        with c3:
            st.markdown('## <font color=#FF97C1>ID # '+'</font>' + ID ,unsafe_allow_html=True)
            record = {ID:{'name':name,'Date of Birth':birth_date,'Address':address,'Gender':gender}}
            df = pd.DataFrame(record)
            st.dataframe(df.transpose(),use_container_width=True)
            if chain == 'Ethereum':
                res = Eth_Invoke(ID,json.dumps(record[ID]))
                if res == 'error':
                    st.error('Upload Error', icon="🚨")
                else:
                    st.success('Upload Successful with tx_hash ' + res, icon="✅")
            if chain == 'Fabric':
                status = Fabric_Invoke(ID,json.dumps(record[ID]))
                if status == 'error':
                    st.error('Upload Error', icon="🚨")
                else:
                    st.success('Upload Successful', icon="✅")
                    
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
        with st.container():
            record = {}
            record[query_ID] = value
            df = pd.DataFrame(record)
            st.dataframe(df.transpose(),use_container_width=True)
        # display record
        pass
    
st.markdown('## Synchronize Identity')
with st.container():
    c1,c2 = st.columns([1,4])
    with c1:
        option = st.radio('Query Chain',['Ethereum to Fabric','Fabric to Ethereum'])
    with c2:
        sync_ID = st.text_input('Sync ID',placeholder='From ' + option)
    sync_button = st.button('sync')
    if sync_button:
        # TODO
        if option == 'Ethereum to Fabric':
            status = Eth_to_Fabric(sync_ID)
            if status == 'error':
                st.error('Synchronize Error', icon="🚨")
            else:
                st.success('Synchronize Successful', icon="✅")
                
        if option == 'Fabric to Ethereum':
            res = Fabric_to_Eth(sync_ID)
            if res == 'error':
                st.error('Upload Error', icon="🚨")
            else:
                st.success('Upload Successful with tx_hash ' + res, icon="✅")
        # display record
        pass