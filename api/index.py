from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io
import base64

app = Flask(__name__)
CORS(app)  # Enable CORS for Flutter app

@app.route('/')
def home():
    return jsonify({
        'status': 'success',
        'message': 'Background Removal API is running!',
        'endpoints': {
            'POST /remove-bg': 'Remove background from image',
            'POST /remove-bg-base64': 'Remove background (base64 input/output)'
        }
    })

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    try:
        # Check if image file is provided
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        image_file = request.files['image']
        
        # Read the image
        input_image = image_file.read()
        
        # Remove background
        output_image = remove(input_image)
        
        # Return the image
        return send_file(
            io.BytesIO(output_image),
            mimetype='image/png',
            as_attachment=False,
            download_name='removed_bg.png'
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/remove-bg-base64', methods=['POST'])
def remove_background_base64():
    try:
        data = request.get_json()
        
        if 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400
        
        # Decode base64 image
        image_data = base64.b64decode(data['image'])
        
        # Remove background
        output_image = remove(image_data)
        
        # Encode back to base64
        output_base64 = base64.b64encode(output_image).decode('utf-8')
        
        return jsonify({
            'status': 'success',
            'image': output_base64
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True)