import os
import base64
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import JSONResponse, Response

load_dotenv()

USE_MOCK = os.getenv("USE_MOCK", "true").lower() == "true"
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
API_BASE = "https://test-api.generio.ai"
HEADERS = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "x-execution-mode": "automatic"
}

app = FastAPI()


@app.get("/")
def root():
    return {"status": "Backend running."}


@app.get("/__test__")
def test():
    return {"success": True}


# --- Shared Utility Functions ---
def upload_asset(image_bytes: bytes) -> str:
    b64_img = base64.b64encode(image_bytes).decode("utf-8")
    data_url = f"data:image/png;base64,{b64_img}"
    response = requests.post(
        f"{API_BASE}/assets",
        headers=HEADERS,
        json={
            "app": "library",
            "file_key": "default",
            "file_data": data_url,
            "file_process": {"mode": "limit", "resolution": 1024},
            "shared": 0
        }
    )
    response.raise_for_status()
    return response.json()["assets"][0]["id"]


def generate_model_from_asset(asset_id: str, prompt: str = "") -> str:
    payload = {
        "app": "sketch",
        "assets": [{"id": asset_id, "file_key": "default"}],
        "seeds": [-1],
        "quality": "high",
        "keep_ratio": 0.95,
        "geometry_adherence": 7.5,
        "material_adherence": 3,
        "material_active": True,
        "additional": {}
    }
    if prompt:
        payload["prompt_positive"] = prompt

    response = requests.post(
        f"{API_BASE}/models/from-assets",
        headers=HEADERS,
        json=payload
    )
    response.raise_for_status()
    return response.json()["assets"][0]["id"]


def share_asset(asset_id: str):
    requests.put(
        f"{API_BASE}/assets/{asset_id}/shared",
        headers=HEADERS,
        json={"shared": 1}
    )


# --- Routes ---
@app.post("/generate/text-to-image")
async def text_to_image(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    if not prompt:
        return {"success": False, "error": "Prompt is required"}

    if USE_MOCK:
        return {
            "success": True,
            "source": "url",
            "id": "mock-image-id",
            "url": f"https://via.placeholder.com/512x512.png?text={prompt.replace(' ', '+')}"
        }

    try:
        response = requests.post(
            f"{API_BASE}/images/from-prompt",
            headers=HEADERS,
            json={
                "app": "generio-ui-dev",
                "prompt_positive": prompt,
                "seeds": [-1],
                "resolution": 1024,
                "diffusion": {
                    "adherence": 2,
                    "denoising": 1,
                    "model": "generio-v1-sfw",
                    "steps": 6
                },
                "alpha": {"active": False, "fill": {"active": False, "margin": 10}},
                "additional": {}
            }
        )
        response.raise_for_status()
        asset_id = response.json()["assets"][0]["id"]
        share_asset(asset_id)
        return {
            "success": True,
            "source": "shared-url",
            "id": asset_id,
            "url": f"{API_BASE}/assets/{asset_id}/shared/files/default/preview.png"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.post("/generate/text-to-model")
async def text_to_model(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    if not prompt:
        return {"success": False, "error": "Prompt is required."}

    if USE_MOCK:
        return {
            "success": True,
            "id": "mock-model-id",
            "url": f"https://via.placeholder.com/512x512.png?text=Model+{prompt.replace(' ', '+')}"
        }

    try:
        response = requests.post(
            f"{API_BASE}/models/from-prompt",
            headers=HEADERS,
            json={
                "app": "generio-ui-dev",
                "prompt_positive": prompt,
                "seeds": [-1],
                "quality": "high",
                "keep_ratio": 0.95,
                "geometry_adherence": 7.5,
                "material_adherence": 3,
                "material_active": True,
                "texture_active": True,
                "additional": {}
            }
        )
        response.raise_for_status()
        asset_id = response.json()["assets"][0]["id"]
        share_asset(asset_id)
        return {"success": True, "id": asset_id}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.post("/generate/sketch-to-model")
async def sketch_to_model(file: UploadFile = File(...), prompt: str = Form(None)):
    if USE_MOCK:
        return {
            "success": True,
            "id": "mock-sketch-id",
            "url": "https://via.placeholder.com/512x512.png?text=SketchModel"
        }

    try:
        image_bytes = await file.read()
        asset_id = upload_asset(image_bytes)
        model_id = generate_model_from_asset(asset_id, prompt or "")
        share_asset(model_id)
        return {"success": True, "id": model_id}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.post("/generate/image-to-model")
async def image_to_model(file: UploadFile = File(...), prompt: str = Form(None)):
    return await sketch_to_model(file, prompt)


@app.get("/proxy-glb/{asset_id}")
def proxy_glb(asset_id: str):
    try:
        url = f"{API_BASE}/assets/{asset_id}/shared/files/default/preview.glb"
        resp = requests.get(url)
        resp.raise_for_status()
        return Response(
            content=resp.content,
            media_type="model/gltf-binary",
            headers={
                "Content-Disposition": f'inline; filename="{asset_id}.glb"',
                "Access-Control-Allow-Origin": "*"
            }
        )
    except Exception as e:
        return Response(content=str(e), media_type="application/json", status_code=502)


@app.get("/status/{asset_id}")
def get_status(asset_id: str):
    try:
        url = f"{API_BASE}/assets/{asset_id}/files/default/status"
        resp = requests.get(url, headers=HEADERS)
        resp.raise_for_status()
        status = resp.json().get("status", "unknown")
        return JSONResponse(
            status_code=200 if status == "ready" else 425 if status == "pending" else 202,
            content={"success": status == "ready", "status": status}
        )
    except Exception as e:
        return JSONResponse(status_code=502, content={"success": False, "error": str(e)})
