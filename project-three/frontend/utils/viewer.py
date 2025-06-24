import streamlit.components.v1 as components


def render_glb_viewer(asset_id: str):
    glb_url = f"http://localhost:8000/proxy-glb/{asset_id}"
    viewer_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <style> body {{ margin: 0; }} </style>
      <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js"></script>
      <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>
      <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    </head>
    <body>
      <div id="viewer" style="width: 100%; height: 500px;"></div>
      <script>
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0xf0f0f0);

        const camera = new THREE.PerspectiveCamera(45, window.innerWidth / 500, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, 500);
        document.getElementById("viewer").appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;

        const hemiLight = new THREE.HemisphereLight(0xffffff, 0x444444, 1.2);
        hemiLight.position.set(0, 20, 0);
        scene.add(hemiLight);

        const dirLight = new THREE.DirectionalLight(0xffffff, 1);
        dirLight.position.set(3, 10, 10);
        scene.add(dirLight);

        const loader = new THREE.GLTFLoader();
        loader.load("{glb_url}",
          function (gltf) {{
            const model = gltf.scene;
            scene.add(model);

            const box = new THREE.Box3().setFromObject(model);
            const center = box.getCenter(new THREE.Vector3());
            const size = box.getSize(new THREE.Vector3());

            // Center the model
            model.position.sub(center);

            // Fit camera to object
            const maxDim = Math.max(size.x, size.y, size.z);
            const fov = camera.fov * (Math.PI / 180);
            const cameraZ = maxDim / (2 * Math.tan(fov / 2));
            camera.position.set(0, maxDim * 0.5, cameraZ * 1.2);
            camera.lookAt(0, 0, 0);
            camera.near = 0.1;
            camera.far = 1000;
            camera.updateProjectionMatrix();
            controls.update();

            function animate() {{
              requestAnimationFrame(animate);
              controls.update();
              renderer.render(scene, camera);
            }}
            animate();
          }},
          undefined,
          function (error) {{
            const msg = document.createElement('div');
            msg.innerText = 'Failed to load model: ' + error;
            msg.style.color = 'red';
            document.getElementById("viewer").appendChild(msg);
          }}
        );
      </script>
    </body>
    </html>
    """
    components.html(viewer_html, height=520)
