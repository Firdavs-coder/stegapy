from flask import Flask, render_template, request, send_file
from PIL import Image
from steganography import Steganography
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'png'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encode', methods=['POST'])
def encode():
    if 'file' not in request.files:
        return 'No file uploaded', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'No file selected', 400
    
    if not allowed_file(file.filename):
        return 'Only PNG files are allowed', 400

    message = request.form.get('message')
    if not message:
        return 'No message provided', 400

    # Save and process the image
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    steg = Steganography(filepath, message)
    steg.encode(os.path.join(app.config['UPLOAD_FOLDER'], 'encoded_' + filename))
    
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], 'encoded_' + filename), as_attachment=True)

@app.route('/decode', methods=['POST'])
def decode():
    if 'file' not in request.files:
        return 'No file uploaded', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'No file selected', 400
    
    if not allowed_file(file.filename):
        return 'Only PNG files are allowed', 400

    # Save and process the image
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    img = Image.open(filepath)

    # Decode the message
    steg = Steganography(filepath)
    message = steg.decode()
    
    return {'message': message}

if __name__ == '__main__':
    app.run(debug=True) 