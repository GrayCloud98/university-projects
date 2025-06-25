import streamlit.components.v1 as components


def render_glb_viewer(asset_id: str):
    glb_url = f"http://localhost:8000/proxy-glb/{asset_id}"
    viewer_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js"></script>
      <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>
    </head>
    <body style="margin: 0; overflow: hidden;">
      <script>
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        const light = new THREE.AmbientLight(0xffffff, 1);
        scene.add(light);

        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
        directionalLight.position.set(5, 10, 7.5);
        scene.add(directionalLight);

        const loader = new THREE.GLTFLoader();
        loader.load("{glb_url}", function(gltf) {{
          console.log("Model loaded:", gltf);
          gltf.scene.position.set(0, 0, 0);
          scene.add(gltf.scene);
          camera.position.z = 10;

          function animate() {{
            requestAnimationFrame(animate);
            renderer.render(scene, camera);
          }}
          animate();
        }}, undefined, function(error) {{
          console.error("Error loading model:", error);
        }});
      </script>
    </body>
    </html>
    """
    components.html(viewer_html, height=600)
