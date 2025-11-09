import streamlit as st
import requests
import time
import io
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from utils.viewer import *

st.set_page_config(page_title="Sketch to Model", layout="centered")
st.title("🎨 Sketch to 3D Model")
st.write("Draw a sketch below and convert it to a 3D model (.glb).")

stroke_color = st.color_picker("🖌️ Choose a stroke color", "#000000")

canvas_result = st_canvas(
    fill_color="rgba(0, 0, 0, 0)",
    stroke_width=6,
    stroke_color=stroke_color,
    background_color="#ffffff",
    height=480,
    width=690,
    drawing_mode="freedraw",
    key="canvas"
)


def is_canvas_empty(image_data):
    if image_data is None:
        return True
    grayscale = np.mean(image_data, axis=2)
    return np.all(grayscale == 255)


def wait_for_model_ready(asset_id: str, max_retries: int = 23, delay: int = 3) -> bool:
    url = f"http://localhost:8000/status/{asset_id}"
    for _ in range(max_retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
            elif response.status_code == 425:
                time.sleep(delay)
                continue
            else:
                return False
        except requests.RequestException:
            time.sleep(delay)
    return False


prompt = st.text_input("✏️ Describe your sketch (optional)", placeholder="e.g. A simple cube")

if st.button("Generate Model"):
    if is_canvas_empty(canvas_result.image_data):
        st.warning("Please draw something on the canvas before generating a model.")
    else:
        with st.spinner("Uploading sketch and generating model..."):
            try:
                img = Image.fromarray(canvas_result.image_data.astype("uint8"))
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format="PNG")
                img_byte_arr.seek(0)

                files = {"file": ("sketch.png", img_byte_arr, "image/png")}
                data = {"prompt": prompt} if prompt else {}

                response = requests.post(
                    "http://localhost:8000/generate/sketch-to-model",
                    files=files,
                    data=data
                )

                if response.status_code != 200:
                    st.error(f"Backend error: {response.status_code}")
                else:
                    data = response.json()
                    if data.get("success") and data.get("id"):
                        asset_id = data["id"]
                        st.info("Waiting for model preview to be ready...")

                        if wait_for_model_ready(asset_id):
                            model_url = f"https://test-api.generio.ai/assets/{asset_id}/shared/files/default/preview.glb"
                            st.success("Model is ready!")
                            st.markdown(f"[📦 Download .glb]({model_url})", unsafe_allow_html=True)
                            st.subheader("🧩 3D Model Preview:")
                            render_glb_viewer(asset_id)
                        else:
                            st.warning("Model not ready yet. Try again shortly.")
                    else:
                        st.error(data.get("error", "Unknown error occurred."))
            except Exception as e:
                st.error(f"Failed to process sketch: {e}")
