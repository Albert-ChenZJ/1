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
from deepface import DeepFace
from chain_operation import Eth_Query,Eth_Invoke,Fabric_Invoke,Fabric_Query,Eth_to_Fabric,Fabric_to_Eth
from numpy import dot
from numpy.linalg import norm

st.set_page_config(layout = "wide")

st.markdown('## Validation')

col1,col2 = st.columns([1,4])
with st.container(): 
        with col1:
            chain = st.radio('Choose a Validation Chain',['Ethereum','Fabric'])
        with col2:
            ID = st.text_input('ID',placeholder=chain)

with st.container():
    c1,c2,c3,c4= st.columns(4)
    with c1:
        img_file_buffer = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    with c2:
        img_string = ''
        if img_file_buffer is not None:
            img_string = ''
            img_embedding_local = []
            img_string = base64.b64encode(img_file_buffer.read())
            image = Image.open(img_file_buffer)
            image.save('./temp_img.jpeg')

            img_embedding_local = DeepFace.represent('./temp_img.jpeg',model_name= 'Facenet')
            print(img_embedding_local)
            
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
    button_validate_label = 'Validate on ' + chain
    button_validate = st.button(button_validate_label)

with st.container():
    if button_validate:
        st.markdown('## <font color=#FF97C1>ID # '+'</font>' + ID ,unsafe_allow_html=True)
        SHA256 = sha256()
        SHA256.update((ID + name + birth_date + address + gender).encode('utf8'))
        SHA_result_local = SHA256.hexdigest()
        record = {ID:{'name':name,'Date of Birth':birth_date,'Address':address,'Gender':gender,'Hash':SHA_result_local,'Face Embedding':img_embedding_local}}
        
        
        df = pd.DataFrame(record)
        st.dataframe(df.transpose(),use_container_width=True)
        if  chain == 'Ethereum':
            res = Eth_Query(ID) # res type String
            value = json.loads(res)
        if chain == 'Fabric':
            value = Fabric_Query(ID)
            
        df = pd.DataFrame(value)
        st.dataframe(df.transpose(),use_container_width=True)
            
        st.markdown('## <font color=#FF97C1>HASH Compare Result  '+'</font>' ,unsafe_allow_html=True)
        print(SHA_result_local)
        print(value)
        Embedding_dict = {ID:{'Local Embedding':img_embedding_local,'Chain Embedding':value['Face Embedding']}}
        hash_dict = {ID:{'Local HASH':SHA_result_local,'Chain HASH':value['Hash']}}
        df = pd.DataFrame(Embedding_dict)
        st.dataframe(df,use_container_width=True)
        df = pd.DataFrame(hash_dict)
        st.dataframe(df,use_container_width=True)
        similarity = dot(img_embedding_local, value['Face Embedding'])/(norm(img_embedding_local)*norm(value['Face Embedding']))
        if similarity > 0.7:
            st.success('Success: Face Verification Passed'+" similarity:" + str(similarity), icon="✅")
        else:
            st.error('Error: Face Verification Failed'+" similarity:" + str(similarity), icon="🚨")
        if SHA_result_local == value['Hash']:
            st.success('Success: HASH Verification Passed', icon="✅")
        else:
            st.error('Error: HASH not equal', icon="🚨")
        # display record
        pass
        