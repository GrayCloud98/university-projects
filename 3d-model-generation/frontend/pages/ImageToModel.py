import streamlit as st
import requests
import time
import numpy as np
from PIL import Image
import cv2
import io
from utils.viewer import render_glb_viewer

st.set_page_config(page_title="Image to Model", layout="centered")
st.title("🖼️ Image to 3D Model")
st.write("Upload an image and turn it into a 3D model (.glb).")


def wait_for_asset_ready(asset_id: str, max_retries=20, delay=3) -> bool:
    status_url = f"http://localhost:8000/status/{asset_id}"
    for _ in range(max_retries):
        try:
            response = requests.get(status_url)
            if response.status_code == 200 and response.json().get("status") == "ready":
                return True
        except Exception:
            pass
        time.sleep(delay)
    return False


def convert_to_sketch(image: Image.Image) -> Image.Image:
    img = np.array(image.convert("RGB"))
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
    edges = cv2.Canny(img_blur, threshold1=50, threshold2=150)
    sketch = cv2.bitwise_not(edges)
    return Image.fromarray(sketch)


st.subheader("📤 Upload Image")

uploaded_file = st.file_uploader("Upload an image (JPG or PNG)", type=["jpg", "jpeg", "png"])
image_prompt = st.text_input("Optional prompt to guide 3D model generation")

if st.button("Generate 3D Model"):
    if not uploaded_file:
        st.warning("Please upload an image first.")
    else:
        with st.spinner("Generating 3D model from your image..."):
            try:
                image = Image.open(uploaded_file)
                sketch_image = convert_to_sketch(image)

                # Convert sketch to bytes
                sketch_buf = io.BytesIO()
                sketch_image.save(sketch_buf, format="PNG")
                sketch_bytes = sketch_buf.getvalue()

                files = {"file": ("sketch.png", sketch_bytes, "image/png")}
                data = {"prompt": image_prompt} if image_prompt else {}

                response = requests.post(
                    "http://localhost:8000/generate/sketch-to-model",
                    files=files,
                    data=data
                )

                if response.status_code != 200:
                    st.error(f"Backend error ({response.status_code}): {response.text}")
                else:
                    result = response.json()
                    if result.get("success") and result.get("id"):
                        model_id = result["id"]
                        st.info("Waiting for the model to be ready...")

                        if wait_for_asset_ready(model_id):
                            model_url = f"https://test-api.generio.ai/assets/{model_id}/shared/files/default/preview.glb"
                            st.success("✅ 3D Model is ready!")
                            st.markdown(f"[🔗 Download .glb model]({model_url})", unsafe_allow_html=True)
                            st.subheader("🧩 3D Model Preview:")
                            render_glb_viewer(model_id)
                        else:
                            st.warning("⚠️ Model is still processing. Please try again later.")
                    else:
                        st.error(result.get("error", "Model generation failed."))
            except Exception as e:
                st.error(f"❌ Request failed: {str(e)}")
