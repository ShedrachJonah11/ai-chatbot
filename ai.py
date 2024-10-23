# ai.py
from fastapi import FastAPI
import openai  # Import OpenAI's API

app = FastAPI()

openai.api_key = 'your-openai-key'  # Replace with your OpenAI API key

@app.post("/paraphrase/")
async def paraphrase_text(text: str):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Paraphrase this: {text}",
        temperature=0.7,
        max_tokens=100
    )
    return {"paraphrased_text": response.choices[0].text.strip()}

@app.post("/generate-image/")
async def generate_image(prompt: str):
    response = openai.Image.create(prompt=prompt)
    return {"image_url": response['data'][0]['url']}
