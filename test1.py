
import os
import json
import streamlit as st
from google.cloud import vision
from PIL import Image
from datetime import datetime
from dateutil.parser import parse as date_parse
from langchain_groq import ChatGroq

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

# Function to extract and convert dates from extracted_text using LLaMA 3 70B
# def extract_and_convert_dates(extracted_text):
#     try:
#         response = llama_model.generate(prompt=extracted_text, max_tokens=200, stop=None)
#         extracted_dates = response.choices[0].text.strip().split("\n")

#         # Convert extracted date strings to datetime objects
#         parsed_dates = []
#         for date_str in extracted_dates:
#             try:
#                 parsed_date = date_parse(date_str)
#                 parsed_dates.append(parsed_date)
#             except ValueError:
#                 st.warning(f"Unable to parse date: {date_str}")

#         return parsed_dates
#     except Exception as e:
#         st.error(f"Error extracting dates: {str(e)}")
#         return []

# Function to extract information using LLM
def extract_info_llm(extracted_text):
    prompt = f"""
    Extract the following information from the text:
    Incident Title, Today's Date, Officer Taking Info, Incident Number, SAR Mission Number, 
    Name (Source), Phone Number (Source), Relationship (Source), 
    Name (Lost Person), Sex (Lost Person), Date of Birth (Lost Person).
    
    Text: {extracted_text}
    
    Format the output as a JSON object with keys: "incident_title", "todays_date", "officer_taking_info", 
    "incident_number", "sar_mission_number", "source_name", "source_phone", "source_relationship", 
    "lost_person_name", "lost_person_sex", "lost_person_dob".
    """

    response = llama_model.generate(prompt=prompt, max_tokens=300, stop=None)
    extracted_info = response.choices[0].text.strip()
    print("this is the output:", extracted_info)
    
    try:
        info_dict = json.loads(extracted_info)
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

        # Extract and convert dates using LLaMA 3 70B
        # extracted_dates = extract_and_convert_dates(extracted_text)
        # st.text("Extracted Dates:")
        # for date_obj in extracted_dates:
        #     st.write(date_obj.strftime("%m/%d/%Y"))

        # Extract information using LLM
        extracted_info = extract_info_llm(extracted_text)
        st.text("Extracted Information:")
        st.write(extracted_info)

        # Manual Entry Form with all fields
        st.header("Manual Entry Form")

        # Incident Information
        st.subheader("Incident Information")
        incident_title = st.text_input("Incident Title", extracted_info.get("incident_title", ""))
        todays_date = st.date_input("Today's Date", date_parse(extracted_info.get("todays_date", "")) if "todays_date" in extracted_info else None)
        time = st.time_input("Time")
        officer_taking_info = st.text_input("Officer Taking Info", extracted_info.get("officer_taking_info", ""))
        incident_number = st.text_input("Incident Number", extracted_info.get("incident_number", ""))
        sar_mission_number = st.text_input("SAR Mission Number", extracted_info.get("sar_mission_number", ""))

        # Source(s) of Information for Questionnaire
        st.subheader("Source(s) of Information for Questionnaire")
        source_name = st.text_input("Name (Source)", extracted_info.get("source_name", ""))
        how_taken = st.text_input("How taken (phone, etc.)")
        source_home_address = st.text_input("Home Address (Source)")
        source_city = st.text_input("City (Source)")
        source_state = st.text_input("State (Source)")
        source_zip = st.text_input("Zip (Source)")
        source_phone = st.text_input("Phone Number (Source)", extracted_info.get("source_phone", ""))
        source_second_phone = st.text_input("2nd Phone Number (Source)")
        source_relationship = st.text_input("Relationship (Source)", extracted_info.get("source_relationship", ""))
        source_contact_now = st.text_input("Where/how to contact now (Source)")
        source_contact_later = st.text_input("Where/how to contact later (Source)")
        informant_belief = st.text_area("What does informant believe happened")

        # Lost Person Information
        st.subheader("Lost Person Information")
        lost_person_name = st.text_input("Name (Lost Person)", extracted_info.get("lost_person_name", ""))
        lost_person_sex = st.selectbox("Sex (Lost Person)", options=["Male", "Female", "Other"], index={"Male": 0, "Female": 1, "Other": 2}.get(extracted_info.get("lost_person_sex", "Male"), 0))
        lost_person_nicknames = st.text_input("Nicknames (Lost Person)")
        lost_person_home_address = st.text_input("Home Address (Lost Person)")
        lost_person_city = st.text_input("City (Lost Person)")
        lost_person_state = st.text_input("State (Lost Person)")
        lost_person_zip = st.text_input("Zip (Lost Person)")
        lost_person_local_address = st.text_input("Local Address (Lost Person)")
        lost_person_local_city = st.text_input("Local City (Lost Person)")
        lost_person_local_state = st.text_input("Local State (Lost Person)")
        lost_person_home_phone = st.text_input("Home Phone Number (Lost Person)")
        lost_person_local_phone = st.text_input("Local Phone Number (Lost Person)")
        lost_person_cell_phone = st.text_input("Cell Phone Number (Lost Person)")
        lost_person_dob = st.date_input("Date of Birth (Lost Person)", date_parse(extracted_info.get("lost_person_dob", "")) if "lost_person_dob" in extracted_info else None)
        lost_person_birthplace = st.text_input("Birthplace (Lost Person)")

        # Physical Description
        st.subheader("Physical Description")
        height = st.text_input("Height")
        weight = st.text_input("Weight")
        age = st.text_input("Age")
        build = st.text_input("Build")
        hair_color = st.text_input("Hair Color")
        hair_length = st.text_input("Hair Length")
        hair_style = st.text_input("Hair Style")
        beard = st.text_input("Beard")
        mustache = st.text_input("Mustache")
        sideburns = st.text_input("Sideburns")
        facial_features = st.text_input("Facial features/shape")
        complexion = st.text_input("Complexion")
        photo_available = st.selectbox("Photo available?", options=["Yes", "No"])
        location_last_seen = st.text_input("Where (location last seen)")
        to_be_returned = st.text_input("To be returned?")
        distinguishing_marks = st.text_input("Distinguishing marks")
        overall_appearance = st.text_area("Overall appearance")
        comments = st.text_area("Comments")

    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        st.exception(e)  # Log detailed exception for debugging
    finally:
        # Clean up: delete the temporary image file
        if os.path.exists("temp_image.jpg"):
            os.remove("temp_image.jpg")
