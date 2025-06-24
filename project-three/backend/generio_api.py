import os
import requests
from dotenv import load_dotenv

load_dotenv()

USE_MOCK = os.getenv("USE_MOCK", "true").lower() == "true"
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
API_BASE = "https://test-api.generio.ai"
HEADERS = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "x-execution-mode": "automatic"
}


def _generate_asset(endpoint: str, payload: dict, preview_type: str, mock_prefix: str, file_ext: str = "png"):
    if USE_MOCK:
        return {
            "success": True,
            "source": "mock",
            "id": "mock-id",
            "url": f"https://via.placeholder.com/512x512.{file_ext}?text={mock_prefix}+{payload.get('prompt_positive', '').replace(' ', '+')}"
        }

    try:
        response = requests.post(f"{API_BASE}{endpoint}", json=payload, headers=HEADERS)
        response.raise_for_status()
        data = response.json()

        assets = data.get("assets", [])
        if not assets or "id" not in assets[0]:
            return {"success": False, "error": "No asset ID returned."}
        asset_id = assets[0]["id"]

        share_response = requests.put(f"{API_BASE}/assets/{asset_id}/shared", json={"shared": 1}, headers=HEADERS)
        share_response.raise_for_status()

        url = f"{API_BASE}/assets/{asset_id}/shared/files/default/{preview_type}.{file_ext}"

        return {
            "success": True,
            "source": "shared-url",
            "id": asset_id,
            "url": url
        }

    except requests.RequestException as e:
        return {"success": False, "error": str(e)}


def generate_image(prompt: str):
    payload = {
        "app": "generio-ui-dev",
        "prompt_positive": prompt,
        "resolution": 1024,
        "diffusion": {
            "adherence": 2,
            "denoising": 1,
            "model": "generio-v1",
            "steps": 6
        }
    }
    return _generate_asset("/images/from-prompt", payload, preview_type="preview", mock_prefix="Image")


def generate_model(prompt: str):
    payload = {
        "app": "generio-ui-dev",
        "prompt_positive": prompt,
        "seeds": [-1],
        "quality": "high",
        "keep_ratio": 0.95,
        "geometry_adherence": 7.5,
        "material_adherence": 3,
        "material_active": True,
        "additional": {}
    }
    return _generate_asset("/models/from-prompt", payload, preview_type="preview", mock_prefix="Model", file_ext="glb")


def check_asset_status(asset_id: str, file_key: str = "default"):
    try:
        response = requests.get(
            f"{API_BASE}/assets/{asset_id}/files/{file_key}/status",
            headers=HEADERS
        )
        response.raise_for_status()
        data = response.json()

        return {
            "success": True,
            "status": data.get("status"),
            "details": data.get("details", "")
        }

    except requests.RequestException as e:
        return {"success": False, "error": str(e)}


def is_model_ready(asset_id: str, file_key: str = "default") -> bool:
    try:
        r = requests.get(f"{API_BASE}/assets/{asset_id}/files/{file_key}/status", headers=HEADERS)
        r.raise_for_status()
        status = r.json().get("status", "")
        return status.lower() == "ready"
    except requests.RequestException:
        return False
