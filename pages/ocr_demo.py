import streamlit as st
from ocr_utils import analyze
image = "./images/real.jpg"

on = st.toggle('Use backup file')
data = 0

st.title("Extracting Text")
st.write("**Using Oracles OCI vision service**")
if on:
        image = "./images/backup.jpg"   
        st.image('./images/backup.jpg')
else:
    image = "./images/real.jpg"
    st.image('./images/real.jpg')

if st.button('Analyze'):
    if on:
        image = "./images/backup.jpg"   
        st.image('./images/backup.jpg')
    else:
        image = "./images/real.jpg"
        st.image('./images/real.jpg')
    data = analyze(image)
    st.write(data)      
else:
    st.write(data)