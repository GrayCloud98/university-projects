import streamlit.components.v1 as components


def render_glb_viewer(asset_id: str, height: int = 600):
    glb_url = f"https://test-api.generio.ai/assets/{asset_id}/shared/files/default/preview.glb"
    html = f"""
    <!-- model-viewer web component -->
    <script type="module"
            src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js">
    </script>

    <model-viewer
      src="{glb_url}"
      alt="3D model"
      auto-rotate
      camera-controls
      exposure="1"
      background-color="#eeeeee"
      style="width:100%; height:{height}px;">
    </model-viewer>
    """
    components.html(html, height=height)
