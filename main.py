from typing import Annotated
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import google.generativeai as genai
from google.generativeai import types
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))

MODEL_NAME = "gemini-2.5-flash"

app = FastAPI()

@app.post("/ai")
async def generate_answer(file: UploadFile = File(...)):
    if file.filename.split(".")[1] not in ["m4a"]:
        return False

    try:
        model = genai.GenerativeModel(MODEL_NAME)

        audio_bytes = await file.read()

        audio_part = {
            "mime_type": file.content_type,
            "data": audio_bytes,
        }

        response = model.generate_content(
            contents=[
                'Descreveao áudio',
                audio_part,
            ]
        )

        print(response.text)
        return {"response": response.text}
    except Exception as e:
        return {"error": str(e)}