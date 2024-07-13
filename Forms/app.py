import streamlit as st
from PIL import Image

# Streamlit interface
st.title("LOST/Missing PERSON QUESTIONNAIRE")

# Section to upload and display image
st.header("Upload Image of Handwritten Form")
uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

# Manual Entry Form
st.header("Manual Entry Form")

# Incident Information
st.subheader("Incident Information")
incident_title = st.text_input("Incident Title")
todays_date = st.date_input("Today's Date")
time = st.time_input("Time")
officer_taking_info = st.text_input("Officer Taking Info")
incident_number = st.text_input("Incident Number")
sar_mission_number = st.text_input("SAR Mission Number")

# Source(s) of Information for Questionnaire
st.subheader("Source(s) of Information for Questionnaire")
source_name = st.text_input("Name (Source)")
how_taken = st.text_input("How taken (phone, etc.)")
source_home_address = st.text_input("Home Address (Source)")
source_city = st.text_input("City (Source)")
source_state = st.text_input("State (Source)")
source_zip = st.text_input("Zip (Source)")
source_phone = st.text_input("Phone Number (Source)")
source_second_phone = st.text_input("2nd Phone Number (Source)")
source_relationship = st.text_input("Relationship (Source)")
source_contact_now = st.text_input("Where/how to contact now (Source)")
source_contact_later = st.text_input("Where/how to contact later (Source)")
informant_belief = st.text_area("What does informant believe happened")

# Lost Person Information
st.subheader("Lost Person Information")
lost_person_name = st.text_input("Name (Lost Person)")
lost_person_sex = st.selectbox("Sex (Lost Person)", options=["Male", "Female", "Other"])
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
lost_person_dob = st.date_input("Date of Birth (Lost Person)")
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
