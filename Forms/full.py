import pyaudio
import json
from openai import OpenAI

client = OpenAI(api_key='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')
from vosk import Model, KaldiRecognizer

# Initialize Vosk model
model_path = "/Users/belalelshenety/SURP/Forms/vosk-model-en-us-daanzu-20200905"
model = Model(model_path)
rec = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

# Set OpenAI API key

# Function to extract fields using GPT-3
def extract_fields_with_llm(text_chunk: str, context: dict) -> dict:
    prompt = f"""
    Extract the following fields from the text:
    Incident Title, Today's Date, Time, Officer Taking Info, Incident Number, SAR Mission Number, Name (Source), Phone Number (Source), Relationship (Source), Where/how to contact now (Source), Lost Person Information, Physical Description.

    Context: {context}

    Text: {text_chunk}

    Provide the information in the following format:
    Incident Title: <value>
    Today's Date: <value>
    Time: <value>
    Officer Taking Info: <value>
    Incident Number: <value>
    SAR Mission Number: <value>
    Name (Source): <value>
    Phone Number (Source): <value>
    Relationship (Source): <value>
    Where/how to contact now (Source): <value>
    Lost Person Information: <value>
    Physical Description: <value>
    """
    response = client.completions.create(model="gpt-3.5-turbo-instruct",
    prompt=prompt,
    max_tokens=300,
    temperature=0.5)

    return response.choices[0].text.strip()

# Function to parse the GPT-3 response
def parse_llm_response(response: str) -> dict:
    fields = {}
    lines = response.split('\n')
    for line in lines:
        if ': ' in line:
            key, value = line.split(': ', 1)
            fields[key.strip()] = value.strip()
    return fields

# Maintain a context buffer
context_buffer = {}

# Function to update the context
def update_context(fields: dict):
    for key, value in fields.items():
        if key and value:
            context_buffer[key] = value

# Function to update form fields incrementally
form_data = {}

def update_form(fields: dict):
    for key, value in fields.items():
        if key and value:
            form_data[key] = value
    print(f"Updated Form Data: {form_data}")

# Main function to process transcription
def process_transcription():
    print("Listening...")
    transcript = ""

    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = rec.Result()
            text_chunk = json.loads(result).get("text", "")
            transcript += text_chunk + " "

            # Process the text chunk with LLM
            fields_response = extract_fields_with_llm(text_chunk, context_buffer)
            fields_dict = parse_llm_response(fields_response)

            # Print extracted fields for demonstration
            print(f"Extracted Fields: {fields_dict}")

            # Update the form incrementally with extracted fields
            update_form(fields_dict)
            # Update context buffer
            update_context(fields_dict)

# Start the transcription and incremental extraction process
process_transcription()
