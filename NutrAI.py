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
        with open('./text/real.txt','w') as extract:
            extract.write(str(ocr))

        with open('./text/real.txt', 'r') as json_file:
            json_ocr= json.load(json_file)

        expression = parse('pages[*].lines[*].text')
        match = expression.find(json_ocr)

        parsed=""
        for match in expression.find(json_ocr):
            parsed += match.value  
        print(ocr)
        print(parsed)

        ingredient_prompt = ''''you are a nutiritionist. your job is to examine a list of ingredients and rank them on a scale of 1-10, 10 being the most healthy. Your response should strictly be in the followding format. do not include anythinig else in your response. Add more elements to the array as needed to accomodate all ingredients in the input. Enclose the ingredient names in your response in single quotes.
Ignore any words in input before ingrediants. Rank every ingredient in the folowing format: 
"ranking" | [['ingredient'1',score1], ['ingredient2'score2], ['ingredient3',score3]] "|" <overallscore>
''' + str(parsed)
        overall_prompt = '''you are a nutiritionist. you job is to examine a list of ingredients and rank them on a scale of 1-10, 10 being the most healthy. Your response should strictly be in the followding format. do not include anythinig else in your response.  Score is the numerial score, reason is one sentense description. 
Ignore any words in input before ingrediants.

Score: <score>
Reason: <one sentence explaining your score"
---

input
''' + str(parsed)
        print(overall_prompt)
        
        print("__________")
        print(parsed)
        print("__________")
        if parsed != "":
            st.text("Getting overall ranking")
            response = co.generate(prompt=overall_prompt,
                                    max_tokens=300, temperature=0)        
            string = response.generations[0].text   
            score = string.split()[1]
            reason = string.split(': ')[2]
            score = score
            st.subheader("Overall Ranking: "+str(score))

            print(reason)

            
            st.text("Getting individual rankings")
            response = co.generate(prompt=ingredient_prompt,
                                    max_tokens=300, temperature=0) 
            
            st.subheader('Individual rankings')
            ingredients= response.generations[0].text

            print(response.generations[0].text)
            split_ingredients = ingredients.split("|")[1]
            in1 = eval(split_ingredients)
            st.dataframe(data = in1, hide_index = True, column_config = {"0":"ingredient", "1": st.column_config.ProgressColumn("score", min_value = 0, max_value = 10, format= "%d") })
            
        else:
            st.text("Sorry there was an error please try taking a more clear photo and try again")
       
                 

        