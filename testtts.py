import pygame
import time
from gtts import gTTS
from playsound import playsound
import threading
import os

# === Load image safely ===
def safe_load(path, size=(400, 400)):
    if not os.path.exists(path):
        print(f"[ERROR] Image not found: {path}")
        pygame.quit()
        exit()
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.scale(img, size)
    print(f"[OK] Loaded: {path}")
    return img

# === Speak + animate ===
def speak(text, lang='hi'):
    tts = gTTS(text=text, lang=lang)
    tts.save("speak.mp3")

    audio_thread = threading.Thread(target=lambda: playsound("speak.mp3"))
    audio_thread.start()

    start_time = time.time()
    estimated_duration = 6
    clock = pygame.time.Clock()

    while time.time() - start_time < estimated_duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill((255, 255, 255))
        screen.blit(face_img, (0, 0))

        if int(time.time() * 10) % 2 == 0:
            screen.blit(mouth_open_img, (0, 0))
        else:
            screen.blit(mouth_closed_img, (0, 0))

        pygame.display.update()
        clock.tick(30)

    if os.path.exists("speak.mp3"):
        os.remove("speak.mp3")

# === Init Pygame ===
pygame.init()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Talking Chatbot Face")

# === Load assets ===
assets_path = r"C:\Users\siddhenshwar\Desktop\arduino-vscodes\sign_language_glovetemp2\assets"
face_img = safe_load(os.path.join(assets_path, "face.png"))
mouth_open_img = safe_load(os.path.join(assets_path, "mouth_open.png"))
mouth_closed_img = safe_load(os.path.join(assets_path, "mouth_closed.png"))

# === Background loop (face stays visible) ===
clock = pygame.time.Clock()
speak_thread = None
text_to_speak = None

# Optional: First greeting
speak("Namaste! Main aapki chatbot hoon. Aap kuch bhi bolne ke liye likhiye.", lang='hi')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # You can later add: key press triggers speak

    screen.fill((255, 255, 255))
    screen.blit(face_img, (0, 0))

    # Keep mouth closed until speak is called
    if speak_thread is not None and speak_thread.is_alive():
        if int(time.time() * 10) % 2 == 0:
            screen.blit(mouth_open_img, (0, 0))
        else:
            screen.blit(mouth_closed_img, (0, 0))
    else:
        screen.blit(mouth_closed_img, (0, 0))

    pygame.display.update()
    clock.tick(30)

    # Optional: Example trigger to test again
    if text_to_speak:
        if speak_thread is None or not speak_thread.is_alive():
            speak_thread = threading.Thread(target=speak, args=(text_to_speak,))
            speak_thread.start()
            text_to_speak = None

    # Optional: You can add voice input or keyboard input here
