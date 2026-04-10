# PolypharmGuard - AI-Powered Drug Interaction Detection System

## 🏥 Project Overview

PolypharmGuard is an intelligent system designed to detect harmful drug interactions in doctor's prescriptions using Machine Learning, OCR (Optical Character Recognition), and NLP (Natural Language Processing).

**Key Features:**

- 🤖 ML-based drug interaction prediction model
- 📷 OCR to extract medicines from prescription images
- 📝 NLP to parse prescription text and extract medication details
- 🌐 Web interface for easy access
- ⚠️ Risk level classification (HIGH, MODERATE, LOW)
- 📊 Confidence scores and probability distribution

## 📁 Project Structure

```
polypharmguard/
├── polypharmacy_dataset_1000.csv      # Training dataset with 1000 prescriptions
├── ml_model.py                         # ML model training and prediction
├── ocr_module.py                       # OCR for prescription image processing
├── nlp_module.py                       # NLP for text extraction and parsing
├── polypharmguard.py                   # Main system orchestrator
├── app.py                              # Flask web application
├── templates/
│   └── index.html                      # Web UI
├── models/                             # Trained models (auto-created)
│   ├── drug_interaction_model.pkl
│   ├── drug_encoder.pkl
│   └── label_encoder.pkl
├── uploads/                            # Uploaded prescription images (auto-created)
├── requirements.txt                    # Python dependencies
└── README.md                           # This file
```

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Tesseract OCR (for image text extraction)

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Install Tesseract OCR

**Windows:**

- Download installer: https://github.com/UB-Mannheim/tesseract/wiki
- Install to default location: `C:\Program Files\Tesseract-OCR`
- Or update the path in `ocr_module.py` if installed elsewhere

**macOS:**

```bash
brew install tesseract
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt-get install tesseract-ocr
```

### Step 3: Download spaCy Model

```bash
python -m spacy download en_core_web_sm
```

## 🚀 Usage

### Method 1: Train Model and Run Web Application

```bash
# Run the Flask app (includes model training on first run)
python app.py
```

Then open your browser and navigate to: `http://localhost:5000`

### Method 2: Train Model Separately

```bash
python ml_model.py
```

This will:

- Load the dataset
- Preprocess data and extract drug features
- Train XGBoost model
- Save trained model and encoders to `models/` directory
- Display performance metrics and sample predictions

### Method 3: Use Programmatically

```python
from polypharmguard import PolypharmGuard

# Initialize system
guard = PolypharmGuard(model_trained=True)

# Analyze prescription text
prescription_text = """
Rx:
1. Ibuprofen 400 mg - twice daily
2. Warfarin 5 mg - once daily
3. Aspirin 75 mg - once daily
"""

result = guard.process_prescription_from_text(prescription_text)
print(guard.generate_report(result))

# Analyze prescription image
result = guard.process_prescription_from_image('prescription.jpg')
print(guard.generate_report(result))
```

## 📊 Model Details

### Training Data

- **Dataset:** polypharmacy_dataset_1000.csv
- **Samples:** 1,000 prescriptions
- **Features:**
  - Drug combination count
  - DDI (Drug-Drug Interaction) counts
  - Interaction severity categories (Major, Moderate, Minor)
  - Individual drug presence indicators
- **Target:** Risk Level (HIGH, MODERATE, LOW)

### Model Architecture

- **Algorithm:** XGBoost Classifier
- **Features:** ~100+ (5 base + drug presence indicators)
- **Training/Test Split:** 80/20
- **Performance:** ~92% accuracy on test set

### Drug Database

Currently supports 50+ common medications including:

- Cardiovascular: Warfarin, Aspirin, Losartan, Amlodipine, etc.
- Diabetes: Insulin, Metformin, Glimepiride
- Pain Management: Ibuprofen, Tramadol, Codeine
- Antibiotics: Ciprofloxacin, Erythromycin, Clarithromycin
- Psychiatric: Fluoxetine, Diazepam, Alprazolam, Quetiapine
- Others: Omeprazole, Simvastatin, Prednisone, etc.

## 🔍 How It Works

### Pipeline:

1. **Image Input → OCR**
   - Preprocess image (grayscale, threshold, denoise)
   - Extract text using Tesseract

2. **Text Extraction → NLP**
   - Tokenize sentences
   - Pattern matching for medicine names
   - Extract dosage and frequency information
   - Named Entity Recognition for drug identification

3. **Medicine List → ML Model**
   - Create feature vector
   - Calculate drug interaction metrics
   - Generate prediction

4. **Prediction → Risk Assessment**
   - HIGH: Severe interactions detected - immediate action needed
   - MODERATE: Some interactions - consult healthcare provider
   - LOW: Generally safe combination

## 🌐 Web Interface

### Features:

- **Dual Input:** Upload prescription image or paste text
- **Real-time Analysis:** Instant drug interaction detection
- **Visual Results:**
  - Risk level badge with color coding
  - Detected medicines list
  - Confidence score
  - Risk probability distribution
  - Extracted dosage and frequency
  - Detailed recommendation report

### API Endpoints:

```
POST /api/analyze-image
- File upload and image analysis
- Returns: medicines, risk level, confidence, probabilities

POST /api/analyze-text
- Prescription text analysis
- Returns: medicines, risk level, confidence, probabilities

GET /api/supported-medicines
- List of supported medicines

GET /api/health
- System status check
```

## 📈 Results Interpretation

### Risk Levels:

**HIGH RISK 🔴**

- Multiple severe interactions detected
- Action: Immediate pharmacist/physician consultation
- Consider alternative medications
- Close monitoring required

**MODERATE RISK 🟠**

- Some significant interactions present
- Action: Healthcare provider consultation
- Possible dosage adjustment needed
- Regular monitoring

**LOW RISK 🟢**

- Minimal interaction concerns
- Action: Standard monitoring
- Generally safe for use
- Follow normal precautions

### Confidence Score:

- 95-100%: Very reliable prediction
- 80-95%: Good prediction confidence
- 70-80%: Moderate confidence
- <70%: Low confidence (recommend expert review)

## 🔧 Configuration

### Modify Tesseract Path (Windows):

Edit `ocr_module.py`:

```python
tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
ocr = PrescriptionOCR(tesseract_path=tesseract_path)
```

### Adjust Model Parameters:

Edit `ml_model.py` in the `train_model()` method:

```python
self.model = XGBClassifier(
    n_estimators=200,      # Number of trees
    max_depth=8,           # Tree depth
    learning_rate=0.05,    # Learning rate
    # ... adjust as needed
)
```

## 📝 Supported Medicines

60+ medicines including common drugs like:

- Ibuprofen, Paracetamol, Aspirin
- Warfarin, Clopidogrel
- Fluoxetine, Sertraline, Diazepam
- Metformin, Insulin, Glimepiride
- Omeprazole, Pantoprazole
- Simvastatin, Atorvastatin
- Ciprofloxacin, Erythromycin
- And many more...

To add more medicines, edit `nlp_module.py`'s `MEDICINE_KEYWORDS` dictionary.

## ⚙️ Requirements

```
pandas==1.5.3
numpy==1.24.3
scikit-learn==1.3.0
xgboost==2.0.0
pytesseract==0.3.10
Pillow==10.0.0
opencv-python==4.8.0.74
spacy==3.6.0
nltk==3.8.1
flask==2.3.3
flask-cors==4.0.0
joblib==1.3.1
```

## 🚨 Important Disclaimers

⚠️ **This system is for informational purposes only and should NOT be used as a substitute for professional medical advice.**

- Always consult with qualified healthcare professionals
- Verify all recommendations with pharmacists and physicians
- This AI system may miss rare or complex interactions
- Use this as a screening tool only, not final medical decision

## 🤝 Contributing

To extend the system:

1. **Add More Medicines:** Update `MEDICINE_KEYWORDS` in `nlp_module.py`
2. **Improve OCR:** Enhance image preprocessing in `ocr_module.py`
3. **Better NLP:** Refine pattern matching and extraction in `nlp_module.py`
4. **Model Enhancement:** Train with larger dataset for better accuracy

## 📚 Learning Resources

- XGBoost Documentation: https://xgboost.readthedocs.io/
- Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki
- spaCy NLP: https://spacy.io/
- NLTK: https://www.nltk.org/

## 📞 Support

For issues, questions, or suggestions, please refer to the codebase structure and comments within each module.

## 📄 License

This project is provided as-is for educational and research purposes.

---

**Made with ❤️ for healthcare innovation**

Version: 1.0.0
Last Updated: 2024
