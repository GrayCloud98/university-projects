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


def generate_image(prompt: str):
    if USE_MOCK:
        return {
            "success": True,
            "source": "mock",
            "url": f"https://via.placeholder.com/512x512.png?text={prompt.replace(' ', '+')}"
        }

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

    try:
        # Step 1: Generate image asset
        gen_response = requests.post(
            f"{API_BASE}/images/from-prompt",
            json=payload,
            headers=HEADERS
        )
        gen_response.raise_for_status()
        gen_data = gen_response.json()

        assets = gen_data.get("assets", [])
        if not assets or "id" not in assets[0]:
            return {"success": False, "error": "No asset ID returned."}

        asset_id = assets[0]["id"]

        # Step 2: Make asset shared
        share_response = requests.put(
            f"{API_BASE}/assets/{asset_id}/shared",
            json={"shared": 1},
            headers=HEADERS
        )
        share_response.raise_for_status()

        # Step 3: Construct public preview image URL
        image_url = f"{API_BASE}/assets/{asset_id}/shared/files/default/preview.png"

        return {
            "success": True,
            "source": "shared-url",
            "url": image_url
        }

    except requests.RequestException as e:
        return {"success": False, "error": str(e)}
