from flask import Flask, request, jsonify, send_file, render_template
from diffusers import StableDiffusionPipeline
import torch
import os
from PIL import Image
from datetime import datetime
import traceback
import huggingface_hub

app = Flask(__name__)

UPLOAD_FOLDER = "input"
OUTPUT_FOLDER = "generated"
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
HUGGINGFACE_TOKEN = "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"  # Replace with your token

# Set up HuggingFace token
huggingface_hub.login(token=HUGGINGFACE_TOKEN)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
C:\Users\medin\Downloads\roomgpt_cpu\backend
try:
    # Update model loading to use token through huggingface_hub
    huggingface_hub.login(token=HUGGINGFACE_TOKEN)
    pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
    pipe.to("cpu")
except Exception as e:
    print(f"Error loading model: {str(e)}")
    raise

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clean_old_files(folder, max_age_hours=24):
    current_time = datetime.now()
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        file_age = current_time - datetime.fromtimestamp(os.path.getctime(filepath))
        if file_age.total_seconds() > (max_age_hours * 3600):
            try:
                os.remove(filepath)
            except Exception:
                pass

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Clean old files
        clean_old_files(UPLOAD_FOLDER)
        clean_old_files(OUTPUT_FOLDER)

        # Validate image file
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        image = request.files['image']
        if not image or not allowed_file(image.filename):
            return jsonify({'error': 'Invalid file type. Allowed types: png, jpg, jpeg'}), 400
        
        if request.content_length > MAX_FILE_SIZE:
            return jsonify({'error': f'File too large. Maximum size: {MAX_FILE_SIZE//1024//1024}MB'}), 400

        # Validate and process prompt
        prompt = request.form.get('prompt', '').strip()
        if not prompt:
            prompt = 'modern interior design'
        if len(prompt) > 500:
            return jsonify({'error': 'Prompt too long. Maximum 500 characters'}), 400

        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        input_path = os.path.join(UPLOAD_FOLDER, f"{timestamp}.png")
        output_path = os.path.join(OUTPUT_FOLDER, f"{timestamp}_output.png")

        # Save input image
        try:
            image.save(input_path)
        except Exception as e:
            return jsonify({'error': 'Failed to save input image', 'details': str(e)}), 500

        # Generate image
        try:
            result = pipe(prompt).images[0]
            result.save(output_path)
        except Exception as e:
            if os.path.exists(input_path):
                os.remove(input_path)
            return jsonify({'error': 'Image generation failed', 'details': str(e)}), 500

        # Return generated image
        try:
            return send_file(output_path, mimetype='image/png')
        except Exception as e:
            return jsonify({'error': 'Failed to send generated image', 'details': str(e)}), 500

    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'details': str(e),
            'traceback': traceback.format_exc()
        }), 500

if __name__ == '__main__':
    app.run(debug=True)







