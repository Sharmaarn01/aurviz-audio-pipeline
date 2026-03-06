import requests
import os

# 1. Create a dummy .wav file locally to simulate an audio recording
dummy_file_path = "hello_read_text.wav"
with open(dummy_file_path, "wb") as f:
    f.write(b"This is just dummy byte data simulating an audio file.")

url = "http://127.0.0.1:8000/api/audio/upload"


simulated_uploads = [
    {"device_id": "device_101", "transcription": "read this text"},
    {"device_id": "device_101", "transcription": "open camera"},
    {"device_id": "device_203", "transcription": "what is the weather"}
]

print("Starting Device Simulation...")

for item in simulated_uploads:

    data = {
        "device_id": item["device_id"],
        "transcription": item["transcription"]
    }
    
    with open(dummy_file_path, "rb") as f:
        files = {"file": (dummy_file_path, f, "audio/wav")}
        

        response = requests.post(url, data=data, files=files)
        
        print(f"\nSent from {item['device_id']}: '{item['transcription']}'")
        print("Response:", response.json())


if os.path.exists(dummy_file_path):
    os.remove(dummy_file_path)

print("\nSimulation Complete!")