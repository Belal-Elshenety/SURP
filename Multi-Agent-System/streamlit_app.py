import streamlit as st
from main import SARCrew  # Import the SARCrew class from main.py
import os

# Set environment variables for API keys
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
os.environ["SERPER_API_KEY"] = st.secrets["SERPER_API_KEY"]

# Define different pages
def page_drug_analysis():
    st.title('Drug Analysis Page')
    
    with st.sidebar:
        st.header('Enter Missing Person Details')
        drugs = st.text_input("Drugs Taken")

    if st.button('Gather Intelligence'):
        if not drugs:
            st.error("Please fill all the fields.")
        else:
            inputs = [drugs]
            research_crew = SARCrew(inputs)
            result = research_crew.run_drug()
            st.subheader("Results of Intelligence Gathering:")
            st.write(result)

def question_answering():
    st.title('Medical Condition Analysis Page')
    
    with st.sidebar:
        st.header('Enter question')
        questions = st.text_area("Any additional questions?")

    if st.button('Gather Intelligence'):
        if not questions:
            st.error("Please fill all the fields.")
        else:
            inputs = [questions]
            research_crew = SARCrew(inputs)
            result = research_crew.run_question()
            st.subheader("Results of Intelligence Gathering:")
            st.write(result)

def page_another_task():
    st.title('Another Task Page')
    st.write("This is another task page. You can add more functionality here.")

# Sidebar for navigation
page = st.sidebar.selectbox("Choose a page", ["Drug analysis", "Medical Condition Analysis", "Form Manager"])

# Show the selected page
if page == "Drug analysis":
    page_drug_analysis()
elif page == "Medical Condition Analysis":
    question_answering()