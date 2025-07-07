import streamlit as st
import streamlit.components.v1 as components


def render_glb_viewer(asset_id: str, height: int = 600):
    speed = st.slider("Rotation speed", 0.1, 5.0, 1.0)
    bg_color = st.color_picker("Background color", "#eeeeee")
    poster_url = st.text_input("Poster image URL (optional)", "")

    glb_url = f"https://test-api.generio.ai/assets/{asset_id}/shared/files/default/preview.glb"
    poster_attr = f' poster="{poster_url}"' if poster_url else ''

    html = f"""
    <!-- model-viewer web component -->
    <script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>

    <style>
      .progress-bar {{
        position: absolute;
        bottom: 10px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(0, 0, 0, 0.5);
        padding: 4px 8px;
        color: #fff;
        border-radius: 4px;
        font-size: 0.9em;
      }}
      .hotspot-label {{
        background: rgba(0, 0, 0, 0.7);
        color: #fff;
        padding: 4px 6px;
        border-radius: 4px;
        pointer-events: none;
        font-size: 0.85em;
      }}
    </style>

    <model-viewer
      src="{glb_url}"
      alt="3D model"
      auto-rotate
      auto-rotate-delay="100"
      auto-rotate-speed="{speed}"
      camera-controls
      exposure="1"
      background-color="{bg_color}"
      environment-image="https://modelviewer.dev/shared-assets/environments/venice_sunset_1k.hdr"
      shadow-intensity="1"{poster_attr}
      style="width:100%; height:{height}px; position: relative;"
    >
      <!-- progress slot -->
      <div slot="progress" class="progress-bar">
        <span id="progress-text">Loading…</span>
      </div>

      <script>
        const mv = document.querySelector('model-viewer');
        const text = document.getElementById('progress-text');
        mv.addEventListener('progress', function(event) {{
          var pct = Math.round(event.detail.totalProgress * 100);
          text.textContent = 'Loading ' + pct + '%';
        }});
      </script>

      <!-- example hotspots -->
      <button slot="hotspot-1" data-position="0m 0.5m 0m" data-normal="0m 1m 0m">Info</button>
      <div slot="hotspot-1-ui" class="hotspot-label">Main feature</div>

      <button slot="hotspot-2" data-position="0.5m 0.2m 0m" data-normal="0m 1m 0m">Detail</button>
      <div slot="hotspot-2-ui" class="hotspot-label">Secondary detail</div>
    </model-viewer>
    """

    components.html(html, height=height)
