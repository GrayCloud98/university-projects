from fastapi import FastAPI, Request
from generio_api import generate_image

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/generate/text-to-image")
async def text_to_image(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    result = generate_image(prompt)
    return result
