import streamlit as st
from PIL import Image
from datetime import datetime
import speech_recognition as sr

# Initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()

# Function to recognize speech and return the text
def recognize_speech():
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            st.write("You said: " + text)
            return text
        except sr.UnknownValueError:
            st.write("Google Speech Recognition could not understand audio")
            return ""
        except sr.RequestError as e:
            st.write(f"Could not request results from Google Speech Recognition service; {e}")
            return ""

# Predefined object with values to fill in the form
predefined_data = {
    "Incident Title": "Sample Incident",
    "Today's Date": "2024-07-12",
    "Time": "14:30:00",
    "Officer Taking Info": "Officer John Doe",
    "Incident Number": "123456",
    "SAR Mission Number": "78910",
    "Source Name": "Jane Doe",
    "How taken": "Phone call",
    "Source Home Address": "123 Main St",
    "Source City": "Anytown",
    "Source State": "CA",
    "Source Zip": "12345",
    "Source Phone": "123-456-7890",
    "Source 2nd Phone": "098-765-4321",
    "Source Relationship": "Friend",
    "Source Contact Now": "123-456-7890",
    "Source Contact Later": "098-765-4321",
    "Informant Belief": "Lost in the woods",
    "Lost Person Name": "John Smith",
    "Lost Person Sex": "Male",
    "Lost Person Nicknames": "Johnny",
    "Lost Person Home Address": "456 Elm St",
    "Lost Person City": "Anytown",
    "Lost Person State": "CA",
    "Lost Person Zip": "67890",
    "Lost Person Local Address": "789 Oak St",
    "Lost Person Local City": "Othertown",
    "Lost Person Local State": "CA",
    "Lost Person Home Phone": "234-567-8901",
    "Lost Person Local Phone": "345-678-9012",
    "Lost Person Cell Phone": "456-789-0123",
    "Lost Person DOB": "1990-01-01",
    "Lost Person Birthplace": "Anytown, CA",
    "Height": "6'0\"",
    "Weight": "180 lbs",
    "Age": "34",
    "Build": "Athletic",
    "Hair Color": "Brown",
    "Hair Length": "Short",
    "Hair Style": "Curly",
    "Beard": "None",
    "Mustache": "None",
    "Sideburns": "None",
    "Facial Features": "Square jaw",
    "Complexion": "Fair",
    "Photo Available": "Yes",
    "Location Last Seen": "Near the river",
    "To Be Returned": "Yes",
    "Distinguishing Marks": "Scar on left arm",
    "Overall Appearance": "Wearing a blue jacket",
    "Comments": "Last seen heading north"
}

# Convert string dates to datetime.date objects
if "Today's Date" in predefined_data:
    predefined_data["Today's Date"] = datetime.strptime(predefined_data["Today's Date"], "%Y-%m-%d").date()
if "Lost Person DOB" in predefined_data:
    predefined_data["Lost Person DOB"] = datetime.strptime(predefined_data["Lost Person DOB"], "%Y-%m-%d").date()

# Convert string time to datetime.time objects
if "Time" in predefined_data:
    predefined_data["Time"] = datetime.strptime(predefined_data["Time"], "%H:%M:%S").time()

# Streamlit interface
st.title("LOST/Missing PERSON QUESTIONNAIRE")

# Section to upload and display image
st.header("Upload Image of Handwritten Form")
uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

# Button to autofill form with predefined data
if st.button("Autofill Form"):
    st.session_state.update(predefined_data)

# Button to trigger dictation
if st.button("Dictate"):
    recognized_text = recognize_speech()
    if recognized_text:
        extracted_data = nlp_extraction.extract_entities(recognized_text)
        st.session_state.update(extracted_data)

# Manual Entry Form
st.header("Manual Entry Form")

# Incident Information
st.subheader("Incident Information")
incident_title = st.text_input("Incident Title", value=st.session_state.get("Incident Title", ""))
todays_date = st.date_input("Today's Date", value=st.session_state.get("Today's Date"))
time = st.time_input("Time", value=st.session_state.get("Time"))
officer_taking_info = st.text_input("Officer Taking Info", value=st.session_state.get("Officer Taking Info", ""))
incident_number = st.text_input("Incident Number", value=st.session_state.get("Incident Number", ""))
sar_mission_number = st.text_input("SAR Mission Number", value=st.session_state.get("SAR Mission Number", ""))

# Source(s) of Information for Questionnaire
st.subheader("Source(s) of Information for Questionnaire")
source_name = st.text_input("Name (Source)", value=st.session_state.get("Source Name", ""))
how_taken = st.text_input("How taken (phone, etc.)", value=st.session_state.get("How taken", ""))
source_home_address = st.text_input("Home Address (Source)", value=st.session_state.get("Source Home Address", ""))
source_city = st.text_input("City (Source)", value=st.session_state.get("Source City", ""))
source_state = st.text_input("State (Source)", value=st.session_state.get("Source State", ""))
source_zip = st.text_input("Zip (Source)", value=st.session_state.get("Source Zip", ""))
source_phone = st.text_input("Phone Number (Source)", value=st.session_state.get("Source Phone", ""))
source_second_phone = st.text_input("2nd Phone Number (Source)", value=st.session_state.get("Source 2nd Phone", ""))
source_relationship = st.text_input("Relationship (Source)", value=st.session_state.get("Source Relationship", ""))
source_contact_now = st.text_input("Where/how to contact now (Source)", value=st.session_state.get("Source Contact Now", ""))
source_contact_later = st.text_input("Where/how to contact later (Source)", value=st.session_state.get("Source Contact Later", ""))
informant_belief = st.text_area("What does informant believe happened", value=st.session_state.get("Informant Belief", ""))

# Lost Person Information
st.subheader("Lost Person Information")
lost_person_name = st.text_input("Name (Lost Person)", value=st.session_state.get("Lost Person Name", ""))
lost_person_sex = st.selectbox("Sex (Lost Person)", options=["Male", "Female", "Other"], index=0 if st.session_state.get("Lost Person Sex", "") == "" else ["Male", "Female", "Other"].index(st.session_state.get("Lost Person Sex", "")))
lost_person_nicknames = st.text_input("Nicknames (Lost Person)", value=st.session_state.get("Lost Person Nicknames", ""))
lost_person_home_address = st.text_input("Home Address (Lost Person)", value=st.session_state.get("Lost Person Home Address", ""))
lost_person_city = st.text_input("City (Lost Person)", value=st.session_state.get("Lost Person City", ""))
lost_person_state = st.text_input("State (Lost Person)", value=st.session_state.get("Lost Person State", ""))
lost_person_zip = st.text_input("Zip (Lost Person)", value=st.session_state.get("Lost Person Zip", ""))
lost_person_local_address = st.text_input("Local Address (Lost Person)", value=st.session_state.get("Lost Person Local Address", ""))
lost_person_local_city = st.text_input("Local City (Lost Person)", value=st.session_state.get("Lost Person Local City", ""))
lost_person_local_state = st.text_input("Local State (Lost Person)", value=st.session_state.get("Lost Person Local State", ""))
lost_person_home_phone = st.text_input("Home Phone Number (Lost Person)", value=st.session_state.get("Lost Person Home Phone", ""))
lost_person_local_phone = st.text_input("Local Phone Number (Lost Person)", value=st.session_state.get("Lost Person Local Phone", ""))
lost_person_cell_phone = st.text_input("Cell Phone Number (Lost Person)", value=st.session_state.get("Lost Person Cell Phone", ""))
lost_person_dob = st.date_input("Date of Birth (Lost Person)", value=st.session_state.get("Lost Person DOB"))
lost_person_birthplace = st.text_input("Birthplace (Lost Person)", value=st.session_state.get("Lost Person Birthplace", ""))

# Physical Description
st.subheader("Physical Description")
height = st.text_input("Height", value=st.session_state.get("Height", ""))
weight = st.text_input("Weight", value=st.session_state.get("Weight", ""))
age = st.text_input("Age", value=st.session_state.get("Age", ""))
build = st.text_input("Build", value=st.session_state.get("Build", ""))
hair_color = st.text_input("Hair Color", value=st.session_state.get("Hair Color", ""))
hair_length = st.text_input("Hair Length", value=st.session_state.get("Hair Length", ""))
hair_style = st.text_input("Hair Style", value=st.session_state.get("Hair Style", ""))
beard = st.text_input("Beard", value=st.session_state.get("Beard", ""))
mustache = st.text_input("Mustache", value=st.session_state.get("Mustache", ""))
sideburns = st.text_input("Sideburns", value=st.session_state.get("Sideburns", ""))
facial_features = st.text_input("Facial features/shape", value=st.session_state.get("Facial Features", ""))
complexion = st.text_input("Complexion", value=st.session_state.get("Complexion", ""))
photo_available = st.selectbox("Photo available?", options=["Yes", "No"], index=0 if st.session_state.get("Photo Available", "") == "" else ["Yes", "No"].index(st.session_state.get("Photo Available", "")))
location_last_seen = st.text_input("Where (location last seen)", value=st.session_state.get("Location Last Seen", ""))
to_be_returned = st.text_input("To be returned?", value=st.session_state.get("To Be Returned", ""))
distinguishing_marks = st.text_input("Distinguishing marks", value=st.session_state.get("Distinguishing Marks", ""))
overall_appearance = st.text_area("Overall appearance", value=st.session_state.get("Overall Appearance", ""))
comments = st.text_area("Comments", value=st.session_state.get("Comments", ""))
