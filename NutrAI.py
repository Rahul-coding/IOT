import streamlit as st
from streamlit_back_camera_input import back_camera_input
from ocr_utils import analyze
from jsonpath_ng import JSONPath, parse
import json
import cohere
import os
from io import StringIO

co = cohere.Client(os.environ.get('COHERE_KEY'))


st.title("NutrAI")
st.text("press on the sqaure to take a photo")
image = st.camera_input(label= "Take a picture of food label")
if image:
    with open('./images/real.jpg', 'wb') as file: #saving as file 
        file.write(image.getvalue())
        file.close()
    st.text("Photo that was taken (new photo will override last one)")
    st.image('./images/real.jpg') # showing the image
    print('file save')  
image = './images/real.jpg'



if st.button('analyze'):
           
        st.text("Sending to OCR")
        ocr = analyze(image)   
        print("__________")
        print(ocr)
        print("__________")
        with open('./text/real.txt','w') as extract:
            extract.write(str(ocr))

        with open('./text/real.txt', 'r') as json_file:
            json_ocr= json.load(json_file)

        expression = parse('pages[*].lines[*].text')
        match = expression.find(json_ocr)

        parsed=""
        for match in expression.find(json_ocr):
            parsed += match.value  

        ingredient_prompt = "give every ingredeient in this list a score from 1-10 with 10 being the helathiest. Only return the score. Give each ingredient an indivdual score  from 1-10. Return in a list format. Give sugary, high carb, and artificaly flavored food, and processed food, items significantly lower rankings. Rank natural and organic foods higher. Here are the ingredients:" + str(parsed)
        overall_prompt = "give an overall health ranking for a food product containing these ingredients. Rank on a scale from 1-10 with 10 being the healthiest. Only return the ranking and no explanation. Return the score in a bigger font than everything else. Give sugary, high carb, and artificaly flavored food, and processed food items significantly lower rankings. Rank natural and organic foods higher."+str(parsed)
        print("__________")
        print(parsed)
        print("__________")
        st.text("**parsed**")
        st.text(parsed)
        
        st.text(overall_prompt)
        st.text("Getting overall ranking")
        response = co.generate(prompt=overall_prompt)        
        st.subheader("Overall Ranking")
        st.write(response.generations[0].text)
        
        st.text("Getting individual rankings")
        response = co.generate(prompt=ingredient_prompt)  
        st.subheader('Individual rankings')
        st.write(response.generations[0].text)

else:
    print('')