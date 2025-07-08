from typing import Optional
from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import StreamingResponse, Response, JSONResponse
from generio_api import *

import requests
import io

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


@app.post("/generate/text-to-model")
async def text_to_model(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    result = generate_model(prompt)
    return result


@app.post("/generate/sketch-to-model")
async def sketch_to_model(file: UploadFile = File(...),
                          prompt: Optional[str] = Form(default=None)
                          ):
    try:
        image_bytes = await file.read()
        result = generate_model_from_sketch(image_bytes, prompt)
        return result
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})


@app.get("/status/{asset_id}")
async def get_status(asset_id: str):
    return check_asset_status(asset_id)


@app.get("/proxy-glb/{asset_id}")
def proxy_glb(asset_id: str):
    if not is_model_ready(asset_id):
        return Response(content="Model not ready for proxying", status_code=425)

    url = f"https://test-api.generio.ai/assets/{asset_id}/shared/files/default/preview.glb"
    try:
        r = requests.get(url)
        r.raise_for_status()

        return Response(
            content=r.content,
            media_type="model/gltf-binary",
            headers={
                "Content-Disposition": f'inline; filename="{asset_id}.glb"',
                "Access-Control-Allow-Origin": "*"
            }
        )
    except requests.RequestException as e:
        print(f"[Proxy Error] Failed to fetch: {url}")
        print(f"[Proxy Error] {e}")
        return Response(content=str(e), media_type="application/json", status_code=502)
