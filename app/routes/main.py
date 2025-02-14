from flask import Blueprint, render_template, request, send_file
from rembg import remove
from PIL import Image
import io
import base64

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/remove-background', methods=['POST'])
def remove_background():
    try:
        # Get the image file from the request
        file = request.files['image']
        
        # Read the image
        input_image = Image.open(file.stream)
        
        # Remove background
        output_image = remove(input_image)
        
        # Convert to base64 for sending back to frontend
        buffered = io.BytesIO()
        output_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return {'status': 'success', 'image': img_str}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 400 