import socket
import csv

# ===== Server setup =====
HOST = "0.0.0.0"   # Listen on all interfaces
PORT = 8888
gesture_label = "Hello"   # Fixed label

# Create TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print(f"[SERVER] Waiting for ESP32 on {HOST}:{PORT}...")
client, addr = server.accept()
print(f"[SERVER] ESP32 connected from: {addr}")

buffer = ""

# Open CSV file for writing (append mode, auto-flush)
with open("gesture_data.csv", "a", newline="") as f:
    writer = csv.writer(f)
    try:
        while True:
            data = client.recv(1024).decode()
            buffer += data

            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                line = line.strip()
                if line:
                    try:
                        values = list(map(float, line.split(",")))
                        if len(values) == 11:   # 11 sensor values
                            values.append(gesture_label)
                            writer.writerow(values)
                            f.flush()  # 🔥 force save to CSV
                            print("[DATA]", values)
                    except ValueError:
                        print("[WARN] Skipping invalid line:", line)

    except KeyboardInterrupt:
        print("\n[STOP] Data collection stopped by user.")
        client.close()
        server.close()
