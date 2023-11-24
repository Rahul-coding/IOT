import streamlit as st
from ocr_utils import analyze
from jsonpath_ng import JSONPath, parse
import json
image = "./images/real.jpg"

on = st.toggle('Use backup file')
data = 0
parsed = ''

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
else:
    st.write(data)


expression = parse('pages[*].lines[*].text')
match = expression.find(data)
for match in expression.find(data):
    parsed += match.value
with open('./text/real.txt', 'wb') as parsed:
     print("parsed saved")
    
