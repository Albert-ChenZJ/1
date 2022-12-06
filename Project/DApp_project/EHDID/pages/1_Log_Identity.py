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
from deepface import DeepFace
# import web3

password = '12345678'
admin_name = 'comp5565'

st.set_page_config(layout = "wide")

st.markdown('## Log Identity')
col1,col2 = st.columns([1,4])
with col1:
        Admin = st.text_input('Admin',placeholder='Input Admin Name')
with col2:
        pwd = st.text_input('Password',placeholder='Input Your Passwork')
flag = False
if Admin == admin_name and pwd == password:
    flag = True
if flag:
    with st.container():

        with col1:
            chain = st.radio('Chain',['Ethereum','Fabric'])
        with col2:
            ID = st.text_input('ID',placeholder=chain)

    with st.container():
        c1,c2,c3,c4= st.columns(4)
        with c1:
            img_file_buffer = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"],accept_multiple_files=False)
        with c2:
            img_string = ''
            if img_file_buffer is not None:
                img_string = ''
                img_embedding = []
                img_string = base64.b64encode(img_file_buffer.read())
                image = Image.open(img_file_buffer)
                image.save('./temp_img.jpeg')

                img_embedding = DeepFace.represent('./temp_img.jpeg',model_name= 'Facenet')
                print(img_embedding)
                print(img_string.hex())
                print(img_file_buffer)
                
                img_array = np.array(image)
                st.image(
                    image,
                    caption=f"ID Photo",
                    use_column_width=True,
                )
        with c3:
            name = st.text_input('Name')
            birth_date = st.date_input('Date of Birth')
            birth_date = datetime.strftime(birth_date,"%Y/%m/%d")
        with c4:
            address = st.text_input('Address')
            gender = st.selectbox('Gender',['Male','Female'])
        button_log_label = 'Log on ' + chain
        button_log = st.button(button_log_label)
        if button_log:
            st.markdown('## <font color=#FF97C1>ID # '+'</font>' + ID ,unsafe_allow_html=True)
            SHA256 = sha256()
            SHA256.update((ID+ name + birth_date + address + gender).encode('utf8'))
            SHA_result = SHA256.hexdigest()
            record = {ID:{'name':name,'Date of Birth':birth_date,'Address':address,'Gender':gender,'Hash':SHA_result,'Face Embedding':img_embedding}}
            upload_content = {'Face Embedding':img_embedding,'Hash':SHA_result}

            
            df = pd.DataFrame(record)
            st.dataframe(df.transpose(),use_container_width=True)
            if chain == 'Ethereum':
                res = Eth_Invoke(ID ,json.dumps(upload_content))
                res = res.replace('"','')
                if res == 'error':
                    st.error('Upload Error', icon="🚨")
                else:
                    st.success('Upload Successful with tx_hash ' + res, icon="✅")
            if chain == 'Fabric':
                status = Fabric_Invoke(ID,json.dumps(upload_content))
                if status == 'error':
                    st.error('Upload Error', icon="🚨")
                else:
                    st.success('Upload Successful', icon="✅")
                    
    st.markdown('## Synchronize Identity')
    with st.container():
        c1,c2 = st.columns([1,4])
        with c1:
            option = st.radio('Synchronize Option',['Ethereum to Fabric','Fabric to Ethereum'])
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