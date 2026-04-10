from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from polypharmguard import PolypharmGuard
import os
import pytesseract
import platform
from datetime import datetime

# Set Tesseract path for Windows
if platform.system() == 'Windows':
    tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(tesseract_path):
        pytesseract.pytesseract.pytesseract_cmd = tesseract_path

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

# Initialize PolypharmGuard
guard = PolypharmGuard(model_trained=True)

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/api/analyze-image', methods=['POST'])
def analyze_image():
    """Analyze prescription image"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file format. Allowed: PNG, JPG, GIF, BMP, TIFF'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], timestamp + filename)
        file.save(filepath)
        
        # Analyze prescription
        result = guard.process_prescription_from_image(filepath)
        
        if not result:
            return jsonify({'error': 'Could not extract medicines from image'}), 400
        
        report = guard.generate_report(result)
        
        # Convert dosages to serializable format
        dosages = [{'amount': float(d['amount']), 'unit': d['unit']} for d in result['dosages']]
        
        return jsonify({
            'success': True,
            'medicines': result['medicines'],
            'risk_level': result['risk_level'],
            'confidence': float(round(result['confidence'], 2)),
            'probabilities': {k: float(round(v, 2)) for k, v in result['probabilities'].items()},
            'dosages': dosages,
            'frequencies': result['frequencies'],
            'report': report
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analyze-text', methods=['POST'])
def analyze_text():
    """Analyze prescription text"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text'].strip()
        
        if not text:
            return jsonify({'error': 'Text cannot be empty'}), 400
        
        # Analyze prescription
        result = guard.process_prescription_from_text(text)
        
        if not result:
            return jsonify({'error': 'Could not extract medicines from text'}), 400
        
        report = guard.generate_report(result)
        
        # Convert dosages to serializable format
        dosages = [{'amount': float(d['amount']), 'unit': d['unit']} for d in result['dosages']]
        
        return jsonify({
            'success': True,
            'medicines': result['medicines'],
            'risk_level': result['risk_level'],
            'confidence': float(round(result['confidence'], 2)),
            'probabilities': {k: float(round(v, 2)) for k, v in result['probabilities'].items()},
            'dosages': dosages,
            'frequencies': result['frequencies'],
            'report': report
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/supported-medicines', methods=['GET'])
def supported_medicines():
    """Get list of supported medicines"""
    medicines = sorted(list(guard.nlp.MEDICINE_KEYWORDS.keys()))
    return jsonify({'medicines': medicines})


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
