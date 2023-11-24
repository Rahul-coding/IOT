

import cohere
import os
import streamlit as st
co = cohere.Client(os.environ.get('COHERE_KEY'))
control =0 
with open('./parsed_data/cheezit.txt') as data:
  control = 1
st.title("LLM - Cohere")
response = co.generate(
  prompt= "Rank only the ingreditens in this JSON on a scale from 1-10, 10 being the healthiest.  Don't rank anything other than ingredients. give every ingredinet a ranking and return in a JSON format" + str(data))
print("________________________________________________________________")
print(response)
st.title("Prompt")
st.text(response.prompt)
st.title("Response")
st.text(response.generations[0].text)


