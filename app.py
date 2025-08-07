from dotenv import load_dotenv
load_dotenv()
import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

genai.configure(api_key= os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input , image, prompt):
    model=genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content([input , image[0] , prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        #read the file in bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type" : uploaded_file.type, # get the mime type of file uploaded 
                "data" : bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("NO file Uploaded")
    
input_prompt = """
    You are an expert in nutritionist where you need to see the food items from the image and calculate the total calories, also provide the details of every food items with calories intake is below format

    1. Item 1 - Number of calories
    2. Item 2 - Number of calories
    -------
    -------
    Also make a table to list all the items with their calories in it.

    if user upload the image of their vegetables and anything related to eating and ask about the recipe to make best food that is rich in calories and nutrition then you respond by doing google seach and give user the best recipe of their image uploaded food.
"""

st.set_page_config(page_title="AI Nutritionist App")

st.header("AI Nutritionist App")

input = st.text_input("Input Prompt: " , key="input")
uploaded_file = st.file_uploader("choose an image of your food ..." , type=['jpg' ,'png' ,'jpeg'])

image=""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image." , use_container_width=True)

submit = st.button("Tell me the total calories")

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt,image_data,input)
    st.subheader("The response is")
    st.write(response)