import streamlit as st
import requests
import time
from utils.viewer import render_glb_viewer

st.title("🔷 3D Model Generator")
st.write("Enter a prompt to generate a 3D model (.glb format).")


def wait_for_proxy_ready(asset_id: str, max_retries: int = 15, delay: int = 3) -> bool:
    proxy_url = f"http://localhost:8000/proxy-glb/{asset_id}"
    for _ in range(max_retries):
        proxy_check = requests.get(proxy_url)
        if proxy_check.status_code == 200:
            return True
        time.sleep(delay)
    return False


prompt = st.text_input("Model Prompt")

if st.button("Generate Model"):
    if not prompt:
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Submitting prompt..."):
            try:
                response = requests.post(
                    "http://localhost:8000/generate/text-to-model",
                    json={"prompt": prompt}
                )
                if response.status_code != 200:
                    st.error(f"Error from backend: {response.status_code}")
                else:
                    data = response.json()
                    if data.get("success") and data.get("id"):
                        asset_id = data["id"]

                        st.info("Waiting for model preview to be ready...")

                        if wait_for_proxy_ready(asset_id):
                            model_url = f"https://test-api.generio.ai/assets/{asset_id}/shared/files/default/preview.glb"
                            st.success("Model is ready!")
                            st.markdown(f"[🔗 Download .glb Model]({model_url})", unsafe_allow_html=True)
                            st.subheader("🧩 3D Model Preview:")
                            render_glb_viewer(asset_id)
                        else:
                            st.warning("Model preview not ready. Try again later.")
                    else:
                        st.error(data.get("error", "Unknown error occurred."))
            except requests.RequestException as e:
                st.error(f"Request failed: {e}")
