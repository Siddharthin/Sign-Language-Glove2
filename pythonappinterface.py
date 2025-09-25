import asyncio
import websockets
import tkinter as tk
from tkinter import messagebox

# ESP32 WebSocket server address (replace with your ESP32's IP)
ESP32_WS_URL = "ws://192.168.1.50:81"  # Example: ws://192.168.1.50:81

class BuzzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ESP32 Buzzer Control")
        self.root.geometry("300x200")
        self.root.resizable(False, False)

        self.buzzer_state = False

        self.label = tk.Label(root, text="Buzzer Status: OFF", font=("Arial", 14))
        self.label.pack(pady=20)

        self.button = tk.Button(root, text="Turn ON", font=("Arial", 14),
                                command=self.toggle_buzzer, bg="green", fg="white")
        self.button.pack(pady=20)

    def toggle_buzzer(self):
        self.buzzer_state = not self.buzzer_state
        state_str = "ON" if self.buzzer_state else "OFF"
        asyncio.run(self.send_command(state_str))
        self.label.config(text=f"Buzzer Status: {state_str}")
        self.button.config(text=f"Turn {'OFF' if self.buzzer_state else 'ON'}",
                           bg="red" if self.buzzer_state else "green")

    async def send_command(self, command):
        try:
            async with websockets.connect(ESP32_WS_URL) as ws:
                await ws.send(command)
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BuzzerApp(root)
    root.mainloop()
