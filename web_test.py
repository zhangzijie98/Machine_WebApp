#streamlit run C:\Users\dell\Desktop\web_test.py
# -*- coding: utf-8 -*-
import streamlit as st
from st_aggrid import AgGrid
import pandas as pd
import pymysql
from sqlalchemy import create_engine
#import asyncio

engine = create_engine('mysql+pymysql://root:zhang1988@10.130.210.142/wq_rs?charset=utf8')

#new_loop = asyncio.new_event_loop()
#asyncio.set_event_loop(new_loop)

uploaded_file = st.file_uploader("请选择要上传的xls格式表格！")
if uploaded_file is not None:
    df1 = pd.read_excel(uploaded_file)
    AgGrid(df1.head(10))
    df1.to_sql(name=str(uploaded_file.name).replace(".xls",""), con=engine, chunksize=1000, if_exists='replace', index=None)
    st.success("上传成功！")
    
    db = pymysql.connect(host="10.130.210.142", user="root", password="zhang1988", database="wq_rs", charset="utf8")
    sql="select * from "+str(uploaded_file.name).replace(".xls","")
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    df2=pd.read_sql(sql,con=db)
    st.success("数据库中的表格内容如下")
    st.dataframe(df2)
    
else:
    st.warning("请上传xls表格！")
