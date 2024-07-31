import os
import json
import streamlit as st
from google.cloud import vision
from PIL import Image
from datetime import datetime
from dateutil.parser import parse as date_parse
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage

# Initialize Google Cloud Vision client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = st.secrets["GOOGLE_APPLICATION_CREDENTIALS"]
client = vision.ImageAnnotatorClient()

# Initialize LLaMA 3 70B
llama_model = ChatGroq(
    temperature=0.7,
    groq_api_key=st.secrets["GROQ_API_KEY"],
    model_name="llama3-70b-8192"
)

# Function to detect text in an image file
def detect_text(path):
    """Detects text in the file."""
    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    # Extract and return the first text annotation (main text detected)
    if texts:
        return texts[0].description
    else:
        return "No text detected."

# Function to extract information using LLM
def extract_info_llm(extracted_text):
    prompt = f"""
    Extract all the key-value pairs from the text and format the output as a JSON object - just the JSON object, with no sentences such as "Here is the extracted data in JSON format:"
    
    Text: {extracted_text}
    
    Format the output as a JSON object where each key is a field name and each value is the corresponding extracted information.
    """

    response = llama_model.generate(messages=[[HumanMessage(prompt)]], max_tokens=1000, stop=None)
    extracted_info = response.generations[0][0].message.content

    try:
        info_dict = json.loads(extracted_info)
        print("this:", info_dict)
        return info_dict
    except json.JSONDecodeError:
        st.error("Failed to parse the extracted information.")
        return {}

# Streamlit interface
st.title("LOST/Missing PERSON QUESTIONNAIRE")

# Section to upload and display image
st.header("Upload Image of Handwritten Form")
uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        # Save the uploaded file temporarily
        with open("temp_image.jpg", "wb") as f:
            f.write(uploaded_file.read())

        # Call detect_text function on the uploaded image
        extracted_text = detect_text("temp_image.jpg")

        # Display extracted text
        st.text("Extracted Text:")
        st.write(extracted_text)

        # Extract information using LLM
        extracted_info = extract_info_llm(extracted_text)
        st.text("Extracted Information:")
        st.write(extracted_info)

        # Dynamically generate form fields based on extracted information
        st.header("Search and Rescue Questionnaire")

        for key, value in extracted_info.items():
            if "date" in key.lower():
                st.date_input(key, date_parse(value) if value else None)
            elif "time" in key.lower():
                st.time_input(key, datetime.strptime(value, "%H:%M").time() if value else None)
            elif "sex" in key.lower(): #change this
                st.selectbox(key, options=["Male", "Female", "Other"], index={"Male": 0, "Female": 1, "Other": 2}.get(value, 0))
            else:
                st.text_input(key, value)

    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        st.exception(e)  # Log detailed exception for debugging
    finally:
        # Clean up: delete the temporary image file
        if os.path.exists("temp_image.jpg"):
            os.remove("temp_image.jpg")
