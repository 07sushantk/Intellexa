import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

try:
    client = genai.Client()
    models = client.models.list()
    for m in models:
        print(m.name)
except Exception as e:
    import google.generativeai as genai_old
    genai_old.configure(api_key=os.environ["GOOGLE_API_KEY"])
    for m in genai_old.list_models():
        print(m.name)
