import streamlit as st
from streamlit_back_camera_input import back_camera_input
st.title("Camera demo")
st.text("press on the sqaure to take a photo")
image = st.camera_input("Take a picture of food label")
if image:
    with open('./images/image.jpg', 'wb') as file: #saving as file 
        file.write(image.getvalue())
        file.close()
    st.text("Photo that was taken (new photo will override last one)")
    st.image('./images/image.jpg') # showing the image
    print('file save')  