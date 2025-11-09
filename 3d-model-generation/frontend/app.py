import streamlit as st
import requests
import time

st.set_page_config(page_title="GenerIO UI", layout="centered")
st.title("🧠 Project GenerIO")
st.write("Welcome to the interface for 3D model generation.")


def display_image(result):
    if not result.get("success"):
        st.error(f"Backend error: {result.get('error', 'Unknown error')}")
        return

    source = result.get("source")
    url = result.get("url")

    if source == "base64":
        st.warning("Base64 not currently supported.")
        return

    elif source in ["url", "shared-url"]:
        if url:
            st.markdown(f"**🔗 [Open Image in New Tab]({url})**", unsafe_allow_html=True)

            for i in range(5):
                try:
                    resp = requests.get(url)
                    if resp.status_code == 200 and resp.headers["Content-Type"].startswith("image"):
                        st.image(resp.content, caption="Generated Image", width=512)
                        return
                except:
                    pass
                time.sleep(2)

            st.warning("The image is still being processed. Try again shortly.")
        else:
            st.warning("No image URL provided.")
    else:
        st.warning("Unknown image source format.")


prompt = st.text_input("Enter a prompt to generate an image:")

if st.button("Generate Image"):
    if not prompt:
        st.warning("Please enter a prompt before generating.")
    else:
        with st.spinner("Generating image..."):
            try:
                response = requests.post(
                    "http://localhost:8000/generate/text-to-image",
                    json={"prompt": prompt}
                )
                if response.status_code == 200:
                    result = response.json()
                    display_image(result)
                else:
                    st.error(f"Backend error: {response.status_code}")
            except requests.RequestException as e:
                st.error(f"Request failed: {e}")
