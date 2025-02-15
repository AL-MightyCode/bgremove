from flask import Blueprint, render_template, request, send_file, jsonify
from rembg import remove
from PIL import Image
import io
import base64
import sys
import traceback

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/remove-background', methods=['POST'])
def remove_background():
    try:
        # Check if file was uploaded
        if 'image' not in request.files:
            print("No image file in request", file=sys.stderr)
            return jsonify({'status': 'error', 'message': 'No image file uploaded'}), 400
        
        file = request.files['image']
        
        # Check if file is empty
        if file.filename == '':
            print("Empty filename", file=sys.stderr)
            return jsonify({'status': 'error', 'message': 'No selected file'}), 400
            
        # Print debug info
        print(f"Processing file: {file.filename}", file=sys.stderr)
        
        # Read the image
        input_image = Image.open(file.stream)
        print(f"Image opened successfully: {input_image.size}", file=sys.stderr)
        
        # Remove background
        print("Removing background...", file=sys.stderr)
        output_image = remove(input_image)
        print("Background removed successfully", file=sys.stderr)
        
        # Convert to base64
        print("Converting to base64...", file=sys.stderr)
        buffered = io.BytesIO()
        output_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        print("Conversion to base64 complete", file=sys.stderr)
        
        return jsonify({
            'status': 'success',
            'image': img_str
        })
        
    except Exception as e:
        print(f"Error in remove_background: {str(e)}", file=sys.stderr)
        print(f"Traceback: {''.join(traceback.format_tb(e.__traceback__))}", file=sys.stderr)
        return jsonify({
            'status': 'error',
            'message': f'Error processing image: {str(e)}'
        }), 500
