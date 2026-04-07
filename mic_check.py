import speech_recognition as sr

def check_mics():
    print("🔍 Searching for Microphones...")
    mics = sr.Microphone.list_microphone_names()
    
    if not mics:
        print("❌ Koi Mic nahi mila! Driver check karo.")
        return

    for index, name in enumerate(mics):
        print(f"🎤 Index {index}: {name}")

    print("\n---------------------------------")
    print("Ab hum check karenge ki kaunsa mic sun raha hai...")
    
    # Har mic ko test karo
    for index, name in enumerate(mics):
        try:
            print(f"\nTesting Index {index} ({name})...")
            r = sr.Recognizer()
            with sr.Microphone(device_index=index) as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                print("    👉 Kuch bolo...")
                audio = r.listen(source, timeout=3)
                print("    ✅ Awaaz mili! (Ye sahi mic hai)")
                print(f"    🎉 CODE MEIN 'device_index={index}' USE KARO!")
                return # Sahi mic mil gaya, ruk jao
        except:
            print("    ❌ Is mic ne kuch nahi suna.")

if __name__ == "__main__":
    check_mics()