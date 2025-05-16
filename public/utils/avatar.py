import streamlit as st
import base64
import json
import math
from PIL import Image
from io import BytesIO

def get_avatar_placeholder():
    """
    Provides HTML/JS code for a simple 3D avatar visualization
    using Three.js loaded from CDN
    """
    avatar_html = """
    <div id="avatar-container" style="width:100%; height:300px; background-color:#1a1a1a; border-radius:10px;"></div>
    <script src="https://cdn.jsdelivr.net/npm/three@0.132.2/build/three.min.js"></script>
    <script>
      // Simple Three.js avatar visualization
      const container = document.getElementById('avatar-container');
      
      // Initialize Three.js scene
      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.1, 1000);
      const renderer = new THREE.WebGLRenderer({ antialias: true });
      renderer.setSize(container.clientWidth, container.clientHeight);
      renderer.setClearColor(0x1a1a1a);
      container.appendChild(renderer.domElement);
      
      // Create lighting
      const ambientLight = new THREE.AmbientLight(0x404040, 2);
      scene.add(ambientLight);
      
      const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
      directionalLight.position.set(1, 1, 1);
      scene.add(directionalLight);
      
      // Create avatar body parts
      function createAvatar() {
        // Create a group to hold all body parts
        const avatar = new THREE.Group();
        
        // Material for body parts - styling più cartoon/stilizzato
        const bodyMaterial = new THREE.MeshToonMaterial({
          color: 0xf1c27d,  // Skin tone
          shininess: 10
        });
        
        // Colori più vivaci per un aspetto cartoon
        const clothesMaterial = new THREE.MeshToonMaterial({
          color: 0x3498db,  // Blu acceso per i vestiti
          shininess: 5
        });
        
        // Head
        const head = new THREE.Mesh(
          new THREE.SphereGeometry(0.25, 32, 32),
          bodyMaterial
        );
        head.position.y = 0.8;
        avatar.add(head);
        
        // Torso
        const torso = new THREE.Mesh(
          new THREE.CylinderGeometry(0.3, 0.25, 0.6, 16),
          clothesMaterial
        );
        torso.position.y = 0.3;
        avatar.add(torso);
        
        // Arms
        const rightArm = new THREE.Mesh(
          new THREE.CylinderGeometry(0.08, 0.08, 0.5, 16),
          bodyMaterial
        );
        rightArm.position.set(0.38, 0.35, 0);
        rightArm.rotation.z = Math.PI / 16;
        avatar.add(rightArm);
        
        const leftArm = new THREE.Mesh(
          new THREE.CylinderGeometry(0.08, 0.08, 0.5, 16),
          bodyMaterial
        );
        leftArm.position.set(-0.38, 0.35, 0);
        leftArm.rotation.z = -Math.PI / 16;
        avatar.add(leftArm);
        
        // Legs
        const rightLeg = new THREE.Mesh(
          new THREE.CylinderGeometry(0.1, 0.1, 0.6, 16),
          clothesMaterial
        );
        rightLeg.position.set(0.15, -0.3, 0);
        avatar.add(rightLeg);
        
        const leftLeg = new THREE.Mesh(
          new THREE.CylinderGeometry(0.1, 0.1, 0.6, 16),
          clothesMaterial
        );
        leftLeg.position.set(-0.15, -0.3, 0);
        avatar.add(leftLeg);
        
        return avatar;
      }
      
      // Add avatar to scene
      const avatar = createAvatar();
      scene.add(avatar);
      
      // Position camera
      camera.position.z = 2.5;
      camera.position.y = 0.5;
      
      // Animation loop
      function animate() {
        requestAnimationFrame(animate);
        
        // Rotate the avatar slowly
        avatar.rotation.y += 0.01;
        
        renderer.render(scene, camera);
      }
      
      // Handle window resize
      window.addEventListener('resize', function() {
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
      });
      
      // Start animation
      animate();
    </script>
    """
    return avatar_html

def update_avatar_measurements(height, weight, measurements=None):
    """
    Updates avatar proportions based on user's measurements
    Returns a dictionary with avatar parameters
    
    Parameters:
    - height: height in cm
    - weight: weight in kg
    - measurements: dict with keys: chest, waist, hips, arms, thighs
    """
    # Default measurements if none provided
    if measurements is None:
        measurements = {
            'chest': 95,
            'waist': 85, 
            'hips': 100,
            'arms': 35,
            'thighs': 55
        }
    
    # Calculate BMI for basic body shape
    bmi = weight / (height/100)**2
    
    # Simple calculations for avatar proportions
    # These would be more sophisticated in a real app
    avatar_params = {
        'head_size': 1.0,  # Base size, adjusted below
        'torso_width': 1.0 * (measurements['chest'] / 95),
        'torso_depth': 1.0 * (measurements['chest'] / 95),
        'torso_height': 1.0 * (height / 175),
        'waist_width': 1.0 * (measurements['waist'] / 85),
        'hip_width': 1.0 * (measurements['hips'] / 100),
        'arm_width': 1.0 * (measurements['arms'] / 35),
        'arm_length': 1.0 * (height / 175),
        'leg_width': 1.0 * (measurements['thighs'] / 55),
        'leg_length': 1.0 * (height / 175),
        'muscularity': 1.0,  # Base value, adjusted below
    }
    
    # Adjust muscularity based on measurements and weight
    # This is a simplified approach
    arm_to_height_ratio = measurements['arms'] / height
    if arm_to_height_ratio > 0.22:  # Arbitrary threshold
        avatar_params['muscularity'] = 1.2
    
    # Adjust head size proportionally to height
    avatar_params['head_size'] = 1.0 * (175 / height)  # Smaller head for taller people
    
    return avatar_params

def get_customized_avatar_html(user_data):
    """
    Returns customized avatar HTML based on user data
    Genera un avatar stilizzato/cartoonish che si adatta alle misure dell'utente
    """
    # Extract measurements from user data
    height = user_data.get('height', 175)
    weight = user_data.get('weight', 75)
    
    # Get measurements from user data if available
    measurements = {
        'chest': user_data.get('chest', 95),
        'waist': user_data.get('waist', 85),
        'hips': user_data.get('hips', 100),
        'arms': user_data.get('arms', 35),
        'thighs': user_data.get('thighs', 55)
    }
    
    # Get avatar parameters
    avatar_params = update_avatar_measurements(height, weight, measurements)
    
    # Convert parameters to JSON for use in JavaScript
    avatar_params_json = json.dumps(avatar_params)
    
    # Customize the avatar HTML with the parameters
    avatar_html = f"""
    <div id="avatar-container" style="width:100%; height:300px; background-color:#1a1a1a; border-radius:10px;"></div>
    <script src="https://cdn.jsdelivr.net/npm/three@0.132.2/build/three.min.js"></script>
    <script>
      // Avatar parameters from user data
      const avatarParams = {avatar_params_json};
      
      // Initialize Three.js scene
      const container = document.getElementById('avatar-container');
      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.1, 1000);
      const renderer = new THREE.WebGLRenderer({{ antialias: true }});
      renderer.setSize(container.clientWidth, container.clientHeight);
      renderer.setClearColor(0x1a1a1a);
      container.appendChild(renderer.domElement);
      
      // Create lighting
      const ambientLight = new THREE.AmbientLight(0x404040, 2);
      scene.add(ambientLight);
      
      const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
      directionalLight.position.set(1, 1, 1);
      scene.add(directionalLight);
      
      // Create avatar body parts with customized parameters
      function createAvatar() {{
        // Create a group to hold all body parts
        const avatar = new THREE.Group();
        
        // Material for body parts - avatar cartoonizzato
        const bodyMaterial = new THREE.MeshToonMaterial({{
          color: 0xf1c27d,  // Skin tone
          shininess: 10
        }});
        
        // Colori più vivaci per un aspetto cartoon
        const clothesMaterial = new THREE.MeshToonMaterial({{
          color: 0x3498db,  // Blu acceso per i vestiti
          shininess: 5
        }});
        
        // Head - adjusted by head_size parameter
        const head = new THREE.Mesh(
          new THREE.SphereGeometry(0.25 * avatarParams.head_size, 32, 32),
          bodyMaterial
        );
        head.position.y = 0.8 * avatarParams.torso_height;
        avatar.add(head);
        
        // Torso - adjusted by torso parameters
        const torso = new THREE.Mesh(
          new THREE.CylinderGeometry(
            0.3 * avatarParams.torso_width, 
            0.25 * avatarParams.waist_width, 
            0.6 * avatarParams.torso_height, 
            16
          ),
          clothesMaterial
        );
        torso.position.y = 0.3;
        avatar.add(torso);
        
        // Arms - adjusted by arm parameters
        const rightArm = new THREE.Mesh(
          new THREE.CylinderGeometry(
            0.08 * avatarParams.arm_width * avatarParams.muscularity, 
            0.08 * avatarParams.arm_width, 
            0.5 * avatarParams.arm_length, 
            16
          ),
          bodyMaterial
        );
        rightArm.position.set(0.38 * avatarParams.torso_width, 0.35, 0);
        rightArm.rotation.z = Math.PI / 16;
        avatar.add(rightArm);
        
        const leftArm = new THREE.Mesh(
          new THREE.CylinderGeometry(
            0.08 * avatarParams.arm_width * avatarParams.muscularity, 
            0.08 * avatarParams.arm_width, 
            0.5 * avatarParams.arm_length, 
            16
          ),
          bodyMaterial
        );
        leftArm.position.set(-0.38 * avatarParams.torso_width, 0.35, 0);
        leftArm.rotation.z = -Math.PI / 16;
        avatar.add(leftArm);
        
        // Legs - adjusted by leg parameters
        const rightLeg = new THREE.Mesh(
          new THREE.CylinderGeometry(
            0.1 * avatarParams.leg_width, 
            0.1 * avatarParams.leg_width, 
            0.6 * avatarParams.leg_length, 
            16
          ),
          clothesMaterial
        );
        rightLeg.position.set(0.15 * avatarParams.hip_width, -0.3, 0);
        avatar.add(rightLeg);
        
        const leftLeg = new THREE.Mesh(
          new THREE.CylinderGeometry(
            0.1 * avatarParams.leg_width, 
            0.1 * avatarParams.leg_width, 
            0.6 * avatarParams.leg_length, 
            16
          ),
          clothesMaterial
        );
        leftLeg.position.set(-0.15 * avatarParams.hip_width, -0.3, 0);
        avatar.add(leftLeg);
        
        return avatar;
      }}
      
      // Add avatar to scene
      const avatar = createAvatar();
      scene.add(avatar);
      
      // Position camera
      camera.position.z = 2.5;
      camera.position.y = 0.5;
      
      // Animation loop
      function animate() {{
        requestAnimationFrame(animate);
        
        // Rotate the avatar slowly
        avatar.rotation.y += 0.01;
        
        renderer.render(scene, camera);
      }}
      
      // Handle window resize
      window.addEventListener('resize', function() {{
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
      }});
      
      // Start animation
      animate();
    </script>
    """
    return avatar_html
