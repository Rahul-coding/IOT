import streamlit as st
from streamlit_back_camera_input import back_camera_input
from ocr_utils import analyze
from jsonpath_ng import JSONPath, parse
import json
import cohere
import os
from io import StringIO

st.title("NutrAI")
st.text("press on the sqaure to take a photo")
image = st.camera_input("Take a picture of food label")
if image:
    with open('./images/real.jpg', 'wb') as file: #saving as file 
        file.write(image.getvalue())
        file.close()
    st.text("Photo that was taken (new photo will override last one)")
    st.image('./images/real.jpg') # showing the image
    print('file save')  
image = "./images/real.jpg"

on = st.toggle('Use backup file', key='U') 
data = 0
parsed = ''

if on:
        image = "./images/backup.jpg"   
        st.image('./images/backup.jpg')
else:
    image = "./images/real.jpg"
    st.image('./images/real.jpg')




co = cohere.Client(os.environ.get('COHERE_KEY'))
data = ""


file_name = './text/real.txt'

if on:
  file_name = './text/backup.txt'

file=open(file_name ,"r")
data = file.read()

if st.button('analyze', key = 'a'):
        with open('./text/real.txt', 'w') as save:
                save.write(str(parsed))  
        st.text("test")
        if on:
            image = "./images/backup.jpg" 
            #st.image('./images/backup.jpg')
            st.text("Sending to OCR")
            data = analyze(image)   
            with open('./text/real.txt','w') as extract:
                extract.write(str(data))

            with open('./text/real.txt', 'r') as json_file:
                json_data = json.load(json_file)

            expression = parse('pages[*].lines[*].text')
            match = expression.find(json_data)

            for match in expression.find(json_data):
                parsed += match.value  
                #st.image('./images/backup.jpg')
            with open('./text/real.txt', 'w') as save:
                save.write(str(parsed))  
                text = "Rank only the ingreditens in this JSON on a scale from 1-10, 10 being the healthiest.  Don't rank anything other than ingredients. give every ingredinet a ranking: " + str(parsed)
                print(text)
            first_text = "Give an health ranking of a food product containing these ingredients on a scale from 1-10 with 10 being the healthiest.Here are the ingredients:"+str(data)
            st.text("Getting overall ranking")
            response = co.generate(
  prompt=first_text)        
            st.subheader("Overall Ranking")
            st.write(response.generations[0].text)
            st.text("Getting individual rankings")
            response = co.generate(
  prompt=first_text)  
            st.subheader('Individual rankings')
            st.write(response.generations[0].text)
            
        else:
            st.text("Sending to OCR")
            data = analyze(image)   
            with open('./text/real.txt','w') as extract:
                extract.write(str(data))

            with open('./text/real.txt', 'r') as json_file:
                json_data = json.load(json_file)

            expression = parse('pages[*].lines[*].text')
            match = expression.find(json_data)

            for match in expression.find(json_data):
                parsed += match.value

    #print(parsed) 
            with open('./text/real.txt', 'w') as save:
                save.write(str(parsed))  
            text = "Rank only the ingreditens in this JSON on a scale from 1-10, 10 being the healthiest.  Don't rank anything other than ingredients. give every ingredinet a ranking: " + str(parsed)
            first_text = "Give an health ranking of a food product containing these ingredients on a scale from 1-10 with 10 being the healthiest.Here are the ingredients:"+str(data)
            st.text("Getting overall ranking")
            response = co.generate(
                 
  prompt=first_text)
            st.subheader("Overall Ranking")
            st.write(response.generations[0].text)
            st.text("Getting individual rankings")
            
            response = co.generate(
  prompt=text
         )
            st.subheader("Individual rankings")
            st.write(response.generations[0].text)
else:
    print('')