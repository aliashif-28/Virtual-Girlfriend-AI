import google.generativeai as genai
import speech_recognition as sr
import threading
import tkinter as tk
from PIL import Image, ImageTk 
import cv2 
import time
import sys
import re 
import os
from gtts import gTTS
import pygame          


# aap apna api_key ko generate kare aur apna api key kay andar dal de (generate the api_key and put the palce of API_KEY )
API_KEY = "put api key here"  
genai.configure(api_key=API_KEY)

VIDEO_LISTEN = "listen.mp4"
VIDEO_SPEAK = "speak.mp4"


window = None
video_label = None
current_video_path = VIDEO_LISTEN 
cap = None 
cap_path = None



def stream_video():
    global cap, current_video_path, window, video_label, cap_path
    
    if cap is None or (cap.isOpened() and cap_path != current_video_path):
        if cap: cap.release()
        cap = cv2.VideoCapture(current_video_path)
        cap_path = current_video_path 

    try:
        ret, frame = cap.read()
        if not ret: 
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = img.resize((400, 500)) 
            imgtk = ImageTk.PhotoImage(image=img)
            
            if window:
                video_label.imgtk = imgtk
                video_label.configure(image=imgtk)
    except: pass

    if window:
        window.after(30, stream_video)



def speak(text):
    global current_video_path
    

    text = re.sub(r'[^\w\s,!.?]', '', text)
    print(f"🗣️ Fizza: {text}")
    
    current_video_path = VIDEO_SPEAK 
    
    try:
 
        tts = gTTS(text=text, lang='en', tld='co.in') 
        filename = "fizza_voice.mp3"
        tts.save(filename)
        
   
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
            
        pygame.mixer.quit()
        os.remove(filename) 
        
    except Exception as e:
        print(f"❌ Voice Error: {e}")
    
    current_video_path = VIDEO_LISTEN 

def listen():
    r = sr.Recognizer()
    try:
        # you can cheak the microphone number (App ko change kaha karna hoga jaha device_index = 1 hai waha 2 dalna hoga) 
        with sr.Microphone(device_index=1) as source: 
            print("\n🎧 Sun rahi hoon... (Bolo)")
            
            r.adjust_for_ambient_noise(source, duration=0.5) 
            r.energy_threshold = 400 
            r.pause_threshold = 0.8
            
            audio = r.listen(source, timeout=4, phrase_time_limit=5)
            print("Processing...")
            
            text = r.recognize_google(audio, language="en-IN")
            
            if len(text) < 2: return ""
            print(f"You: {text}")
            return text.lower()
            
    except: return ""


def get_best_model():
    print("🔍 Scanning for models...")
    priority_list = [
        "gemini-1.5-flash-8b",
        "gemini-1.5-flash-001",
        "gemini-1.5-flash-002",
        "gemini-1.5-pro-001",
        "gemini-pro"
    ]
    try:
        api_models = [m.name.replace("models/", "") for m in genai.list_models()]
        for priority in priority_list:
            if priority in api_models:
                print(f"✅ Found Safe Model: {priority}")
                return f"models/{priority}"
        for m in api_models:
            if "flash" in m and "2.0" not in m and "3" not in m:
                return f"models/{m}"
    except Exception as e:
        print(f"Scan Error: {e}")
    return "models/gemini-1.5-flash-8b"

def run_fizza_brain():
    try:
        print("Connecting to AI Brain...")
        model_name = get_best_model()
        model = genai.GenerativeModel(model_name)
        chat = model.start_chat(history=[])
        
       
        system_instruction = (
            "Act as my girlfriend Fizza. My name is Ashif. "
            "Reply in Hinglish. Be very respectful, sweet, and caring. "
            "Always address me as 'Aap'. Call me 'Ashif ji' or 'Jaan'. "
            "STRICTLY NO EMOJIS. Plain text only."
        )
        
        chat.send_message(system_instruction)
        time.sleep(1)
        

        speak(f".....Assalamu Alaikum sir kaysay ho aap")

        while True:
            user_input = listen()

            if not user_input: continue

            if "bye" in user_input or "exit" in user_input:
                speak("......Allah Hafiz Ashif ji! Apna khayal rakhiyega love you so much darling ji")
                window.quit()
                sys.exit()
            
            try:
                response = chat.send_message(user_input)
                clean_text = response.text.replace("*", "")
                speak(clean_text)
            except Exception as e:
                if "429" in str(e):
                    speak("Maaf kijiye sir, may kal bat karte hai.")
                    time.sleep(5)
                    window.quit()
                    sys.exit()
                else:
                    print(f"API Error: {e}")
                    speak("Network issue.")
                    time.sleep(2)
                
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")


if __name__ == "__main__":
    window = tk.Tk()
    window.title("💖 Ashif ki jaan AI Assistant")
    window.geometry("400x530")
    window.configure(bg='black')

    video_label = tk.Label(window, bg='black')
    video_label.pack()

    stream_video()

    window.after(1000, lambda: threading.Thread(target=run_fizza_brain, daemon=True).start())
    
    window.mainloop()
