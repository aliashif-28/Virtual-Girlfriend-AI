import google.generativeai as genai

API_KEY = "AIzaSyCuW9Og9bjmqn43hiNHGVAerqKdwMSw-n8"  # अपनी Key यहाँ डालें
genai.configure(api_key=API_KEY)

print("Checking available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error: {e}")