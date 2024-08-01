# import pyaudio
# import os
# from vosk import Model, KaldiRecognizer

# # Specify the path to the Vosk model
# model_path = "/Users/belalelshenety/SURP/Forms/vosk-model-en-us-daanzu-20200905"

# # Ensure the model directory exists
# if not os.path.exists(model_path):
#     print(f"Model path '{model_path}' does not exist. Please download and extract the model.")
#     exit(1)

# # Initialize the Vosk model
# model = Model(model_path)
# rec = KaldiRecognizer(model, 16000)

# # Initialize PyAudio
# p = pyaudio.PyAudio()
# stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
# stream.start_stream()

# print("Listening...")

# # Process audio stream
# while True:
#     data = stream.read(4000, exception_on_overflow=False)
#     if len(data) == 0:
#         break
#     if rec.AcceptWaveform(data):
#         print(rec.Result())
#     else:
#         print(rec.PartialResult())

# print(rec.FinalResult())
import pyaudio
import os
import json
from vosk import Model, KaldiRecognizer

# Specify the path to the Vosk model
model_path = "/Users/belalelshenety/SURP/Forms/model"

# Ensure the model directory exists
if not os.path.exists(model_path):
    print(f"Model path '{model_path}' does not exist. Please download and extract the model.")
    exit(1)

# Initialize the Vosk model
model = Model(model_path)
rec = KaldiRecognizer(model, 16000)

# Initialize PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

print("Listening...")

# Initialize an empty string to store the transcription
transcript = ""
previous_partial_text = ""

# Process audio stream
try:
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = rec.Result()
            text = json.loads(result).get("text", "")
            transcript += text + " "
            # Clear the current line and print the updated transcript
            print(f"\r{transcript}", end="", flush=True)
        else:
            partial_result = rec.PartialResult()
            partial_text = json.loads(partial_result).get("partial", "")
            if partial_text != previous_partial_text:
                # Clear the current line and print the updated partial transcript
                print(f"\r{transcript}{partial_text}", end="", flush=True)
                previous_partial_text = partial_text
except KeyboardInterrupt:
    # Handle KeyboardInterrupt to gracefully exit
    pass

final_result = rec.FinalResult()
final_text = json.loads(final_result).get("text", "")
transcript += final_text
print(f"\r{transcript}", end="")
