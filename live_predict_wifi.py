import socket
import joblib
import numpy as np
import pandas as pd
from gtts import gTTS
from playsound import playsound
import os
import time

# === Constants ===
LANGUAGE = 'hi'   # change to 'en' for English
PORT = 8888
HOST = '0.0.0.0'  # Listen on all interfaces

# === Speak Function ===
def speak_text(text, lang='hi'):
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save("speak.mp3")
        playsound("speak.mp3")
    except Exception as e:
        print(f"[TTS ERROR] {e}")
    finally:
        if os.path.exists("speak.mp3"):
            os.remove("speak.mp3")

# === Load ML Model ===
print("[INFO] Loading ML model...")
model_path = r"C:\Users\siddhenshwar\Desktop\arduino-vscodes\sign_language_glovetemp2\gesture_model.pkl"
model = joblib.load(model_path)

# Ensure correct feature order
feature_names = [
    'flex1', 'flex2', 'flex3', 'flex4', 'flex5',
    'acc_x', 'acc_y', 'acc_z',
    'gyro_x', 'gyro_y', 'gyro_z'
]

# === Setup Socket Server ===
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

def wait_for_connection():
    print(f"[INFO] Waiting for ESP32 to connect on {HOST}:{PORT}...")
    while True:
        try:
            client, addr = server_socket.accept()
            print(f"[CONNECTED] ESP32 connected from: {addr}")
            client.settimeout(15)
            return client
        except Exception as e:
            print(f"[ACCEPT ERROR] {e}")
            time.sleep(2)

client_socket = wait_for_connection()

# === Main Loop ===
while True:
    try:
        data = client_socket.recv(1024).decode().strip()
        if not data:
            continue
        print(f"[RECEIVED] {data}")

        try:
            parts = list(map(float, data.split(',')))
        except ValueError:
            print("[FORMAT ERROR] Invalid float values")
            continue

        if len(parts) != len(feature_names):
            print(f"[WARN] Expected {len(feature_names)} values, got {len(parts)}")
            continue

        input_df = pd.DataFrame([parts], columns=feature_names)
        prediction = model.predict(input_df)[0]
        print(f"[PREDICTED] {prediction}")

        speak_text(prediction, lang=LANGUAGE)
        client_socket.sendall((prediction + '\n').encode())

    except (socket.timeout, ConnectionResetError, socket.error):
        print("[RECONNECTING] ESP32 disconnected or timeout. Waiting again...")
        client_socket = wait_for_connection()
    except Exception as e:
        print(f"[ERROR] {e}")
        break
