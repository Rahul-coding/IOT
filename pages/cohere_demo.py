import cohere
import os
import streamlit as st
co = cohere.Client(os.environ.get('COHERE_KEY'))

st.title("LLM - Cohere")
#response = co.generate(
 # prompt= "")

