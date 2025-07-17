import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

models = genai.list_models()

for model in models:
    print(f"✅ Model ID: {model.name}")
    print(f"   Supported Methods: {model.supported_generation_methods}\n")
