from flask import Blueprint, render_template, request, send_file, jsonify
from rembg import remove
from PIL import Image
import io
import base64
import sys
import traceback
import os
import time

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
        
        # Read the image with error handling
        try:
            input_image = Image.open(file.stream)
            print(f"Image opened successfully: {input_image.size}", file=sys.stderr)
        except Exception as e:
            print(f"Error opening image: {str(e)}", file=sys.stderr)
            return jsonify({'status': 'error', 'message': 'Invalid image file'}), 400
        
        # Remove background with timeout and retry
        max_retries = 3
        retry_count = 0
        while retry_count < max_retries:
            try:
                print(f"Attempt {retry_count + 1}: Removing background...", file=sys.stderr)
                output_image = remove(input_image)
                print("Background removed successfully", file=sys.stderr)
                break
            except Exception as e:
                retry_count += 1
                if retry_count == max_retries:
                    print(f"Failed to remove background after {max_retries} attempts: {str(e)}", file=sys.stderr)
                    return jsonify({'status': 'error', 'message': 'Failed to process image. Please try again.'}), 500
                print(f"Attempt {retry_count} failed, retrying in 5 seconds...", file=sys.stderr)
                time.sleep(5)
        
        # Convert to base64
        try:
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
            print(f"Error in base64 conversion: {str(e)}", file=sys.stderr)
            return jsonify({
                'status': 'error',
                'message': 'Error converting processed image'
            }), 500
            
    except Exception as e:
        print(f"Error in remove_background: {str(e)}", file=sys.stderr)
        print(f"Traceback: {''.join(traceback.format_tb(e.__traceback__))}", file=sys.stderr)
        return jsonify({
            'status': 'error',
            'message': f'Error processing image: {str(e)}'
        }), 500
