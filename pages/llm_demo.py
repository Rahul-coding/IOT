

import cohere
import os
import streamlit as st
from io import StringIO

on = st.toggle('Use backup file')
co = cohere.Client(os.environ.get('COHERE_KEY'))
data = ""
st.title("Ranking")
st.write("**Using Coheres Large Language Model**")

text = "Rank only the ingreditens in this JSON on a scale from 1-10, 10 being the healthiest.  Don't rank anything other than ingredients. give every ingredinet a ranking and return in a JSON format: " + str(data)
file_name = './text/real.txt'

if on:
  file_name = './text/backup.txt'

file=open(file_name ,"r")
data = file.read()
st.subheader("Prompt")
st.write(text+data)
text+= data    
if st.button('analyze'):
    if on:
        response = co.generate(
  prompt= text
        )
        st.subheader("Response")
        st.write(response.generations[0].text)
    else:
         response = co.generate(
  prompt=text
         )
         st.subheader("Response")
         st.write(response.generations[0].text)



