import os
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()

GOOGLE_API_KEY = os.getenv('API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
generation_config = {
  "temperature": 0,
  "top_p": 1,
  "top_k": 45,
  "max_output_tokens": 4096,
}
model = genai.GenerativeModel(model_name="gemini-pro", generation_config=generation_config)
chat = model.start_chat(history=[])
def gemini_response(text):
    try:
        response = chat.send_message(text)
        return response.text
    except:
        return "Error in gemini response"
