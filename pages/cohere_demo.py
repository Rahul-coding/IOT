

import cohere
import os
import streamlit as st
co = cohere.Client(os.environ.get('COHERE_KEY'))
control =0 
with open('/workspaces/stem-fair/parsed_data/cheezit.py') as data:
  control = 1

st.title("LLM - Cohere")
response = co.generate(
  prompt= " Rank only the ingreditens in this JSON on a scale from 1-10, 10 being the healthiest.  Don't rank anything other than ingredients. Rank every ingredinet and return in a list format" + str(data))
st.write(response)

