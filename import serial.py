import socket
import joblib

# Load trained model
model = joblib.load("gesture_model.pkl")

# Create server socket
HOST = '0.0.0.0'
PORT = 8888

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print(f"✅ Waiting for ESP32 to connect on {HOST}:{PORT}...")

client, addr = server.accept()
print(f"📶 ESP32 connected from: {addr}")

while True:
    try:
        data = client.recv(1024).decode().strip()
        if data:
            print("📦 Received:", data)

            values = list(map(float, data.split(",")))
            if len(values) == 11:
                prediction = model.predict([values])[0]
                print("🤖 Predicted Gesture:", prediction)

                # Send back prediction to ESP32
                client.sendall((prediction + "\n").encode())

    except Exception as e:
        print("❌ Error:", e)
