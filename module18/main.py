import pandas as pd
import  streamlit as st

st.header("displaying dataframes")

data = pd.DataFrame({
'Name': ['dreni', 'gerti', 'deon'],
 'Age' : ['16','15','16'],
  'city':['prishtina','prizren','ferizaj']


})

st.dataframe(data)

