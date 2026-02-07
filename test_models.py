import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("LLM_API_KEY")

if not API_KEY:
    print("API Key not found")
    exit()

genai.configure(api_key=API_KEY)

print("Listing available models:\n")

try:
    for model in genai.list_models():
        print(model.name)
except Exception as e:
    print("Error:", e)
