import streamlit as st
import streamlit_toggle as tog
import cohere 
import os
co = cohere.Client(os.environ.get('COHERE_KEY'))
control = 0
on = st.toggle('Use backup file')
with open('./parsed_data/cheezit.txt') as data:
  control = 1
control = 1


if st.button('analyze'):
    if on:
        response = co.generate(
  prompt= "Rank only the ingreditens in this JSON on a scale from 1-10, 10 being the healthiest.  Don't rank anything other than ingredients. give every ingredinet a ranking and return in a JSON format" + str(data))
        print(response.generations[0].text)
    else:
         response = co.generate(
  prompt= "Rank only the ingreditens in this JSON on a scale from 1-10, 10 being the healthiest.  Don't rank anything other than ingredients. give every ingredinet a ranking and return in a JSON format" + str(data))
         
else:
    st.write("Rank only the ingreditens in this JSON on a scale from 1-10, 10 being the healthiest.  Don't rank anything other than ingredients. give every ingredinet a ranking and return in a JSON format + str(data)")
