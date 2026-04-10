# PolypharmGuard - Complete Installation & Testing Guide

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Verification & Testing](#verification--testing)
4. [First Run](#first-run)
5. [Troubleshooting](#troubleshooting)

---

## 💻 System Requirements

### Minimum Requirements

- **OS:** Windows 10+, macOS 10.14+, or Ubuntu 18.04+
- **Python:** 3.8 or higher
- **RAM:** 4GB minimum (8GB recommended)
- **Disk Space:** 2GB for dependencies and models
- **Internet:** Required for downloading ML dependencies

### Recommended Setup

- **OS:** Windows 11 / macOS 12+ / Ubuntu 20.04+
- **Python:** 3.10 or higher
- **RAM:** 8GB+
- **Disk Space:** 4GB+
- **GPU:** NVIDIA GPU for faster training (optional)

---

## 🔧 Installation Steps

### Step 1: Verify Python Installation

```bash
# Check Python version
python --version
# Should show: Python 3.8 or higher

# Check pip
pip --version
# Should show: pip version
```

**If you don't have Python:**

- Download from: https://www.python.org/downloads/
- During installation, check "Add Python to PATH"

---

### Step 2: Clone/Copy Project

```bash
# Navigate to project directory
cd C:\Users\akhil\Desktop\polypharmguard

# Verify files exist
dir  # Windows
# or
ls   # macOS/Linux
```

Expected files:

```
polypharmacy_dataset_1000.csv
requirements.txt
ml_model.py
ocr_module.py
nlp_module.py
polypharmguard.py
app.py
train_model.py
demo.py
config.py
README.md
QUICKSTART.md
PROJECT_SUMMARY.md
```

---

### Step 3: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

---

### Step 4: Install Python Dependencies

```bash
# Upgrade pip, setuptools, wheel
pip install --upgrade pip setuptools wheel

# Install project dependencies
pip install -r requirements.txt
```

This will install:

- pandas, numpy, scikit-learn
- XGBoost, Pillow, OpenCV
- Flask, Flask-CORS
- pytesseract, spacy, nltk
- joblib, requests

Installation time: ~5-10 minutes depending on internet speed

---

### Step 5: Install Tesseract OCR

#### Windows Installation

1. **Download Installer:**
   - Go to: https://github.com/UB-Mannheim/tesseract/wiki
   - Download: `tesseract-ocr-w64-setup-v5.x.x.exe`

2. **Run Installer:**
   - Double-click the installer
   - Choose default installation path: `C:\Program Files\Tesseract-OCR`
   - Complete installation

3. **Verify Installation:**
   ```bash
   "C:\Program Files\Tesseract-OCR\tesseract.exe" --version
   # Should show version information
   ```

#### macOS Installation

```bash
# Install via Homebrew
brew install tesseract

# Verify
tesseract --version
```

#### Linux Installation (Ubuntu/Debian)

```bash
# Install Tesseract
sudo apt-get update
sudo apt-get install tesseract-ocr

# Verify
tesseract --version
```

#### Linux Installation (Fedora/CentOS)

```bash
sudo yum install tesseract

# Verify
tesseract --version
```

---

### Step 6: Download spaCy Model

```bash
# Download English model (~50MB)
python -m spacy download en_core_web_sm

# Verify
python -c "import spacy; spacy.load('en_core_web_sm'); print('✓ spaCy model loaded')"
```

---

### Step 7: Configure Tesseract Path (if needed)

If Tesseract is installed in a non-default location, update `ocr_module.py`:

```python
# At the top of ocr_module.py, modify:
pytesseract.pytesseract.pytesseract_cmd = r'C:\Your\Path\To\tesseract.exe'
```

Or use `config.py`:

```python
# In config.py, set:
TESSERACT_PATH = r'C:\Your\Path\To\tesseract.exe'
```

---

## ✅ Verification & Testing

### Test 1: Verify All Imports

```bash
python -c "
import pandas
import numpy
import sklearn
import xgboost
import flask
import pytesseract
import spacy
import nltk
print('✓ All core packages imported successfully')
"
```

Expected output: `✓ All core packages imported successfully`

---

### Test 2: Verify Tesseract

```bash
python -c "
from ocr_module import PrescriptionOCR
print('✓ OCR module initialized')
"
```

**If you get an error:**

- Ensure Tesseract is installed
- Check `TESSERACT_PATH` in `config.py` or `ocr_module.py`

---

### Test 3: Verify NLP

```bash
python -c "
from nlp_module import MedicineNLP
nlp = MedicineNLP()
result = nlp.extract_medicines('Take Ibuprofen 400mg twice daily')
print(f'✓ Medicines extracted: {result}')
"
```

Expected output: `✓ Medicines extracted: ['ibuprofen']`

---

### Test 4: Train ML Model

```bash
python train_model.py
```

**Expected output:**

```
Loading dataset...
Dataset shape: (1000, 8)

Preprocessing data...
Total unique drugs: 50+

Training XGBoost model...
Model Accuracy: 0.92xx

✓ Model training completed successfully!
Model files saved:
  - models/drug_interaction_model.pkl
  - models/drug_encoder.pkl
  - models/label_encoder.pkl
```

**Training time:** 1-5 minutes depending on your system

---

### Test 5: Run Demo

```bash
python demo.py
```

**Expected output:**

```
DEMO 1: Prescription Text Analysis
[Shows analysis results]

DEMO 2: Supported Medicines
[Lists 50+ medicines]

DEMO 3: Extract Medicine Details
[Shows extracted medicines, dosages, frequencies]

DEMO 4: Drug Interaction Checking
[Shows 3 test cases with risk assessments]

✓ All demos completed successfully!
```

---

### Test 6: Test Web Application

```bash
python app.py
```

**Expected output:**

```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://localhost:5000
```

Then open browser: **http://localhost:5000**

You should see the PolypharmGuard web interface!

---

## 🚀 First Run

### Scenario 1: Analyze Text Prescription

1. Open: http://localhost:5000
2. Go to "📝 Prescription Text" tab
3. Paste:
   ```
   Rx:
   1. Ibuprofen 400 mg - twice daily
   2. Warfarin 5 mg - once daily
   3. Aspirin 75 mg - once daily
   ```
4. Click "Analyze Text"
5. View results!

### Scenario 2: Analyze Image Prescription

1. Open: http://localhost:5000
2. Go to "📷 Prescription Image" tab
3. Click or drag prescription image
4. Click "Analyze Image"
5. View results!

### Scenario 3: Use Programmatically

```bash
python -c "
from polypharmguard import PolypharmGuard

guard = PolypharmGuard(model_trained=True)
result = guard.process_prescription_from_text('Ibuprofen, Warfarin, Aspirin')
print(f'Risk Level: {result[\"risk_level\"]}')
print(f'Confidence: {result[\"confidence\"]}%')
"
```

---

## 🐛 Troubleshooting

### Issue 1: "ModuleNotFoundError: No module named 'xgboost'"

**Solution:**

```bash
pip install xgboost
```

### Issue 2: "TesseractNotFoundError"

**Solution:**

- Verify Tesseract is installed
- Update path in `ocr_module.py`
- Windows: Install to `C:\Program Files\Tesseract-OCR`

### Issue 3: "No module named 'spacy'"

**Solution:**

```bash
pip install spacy
python -m spacy download en_core_web_sm
```

### Issue 4: "Model files not found"

**Solution:**

```bash
python train_model.py  # Train model first
```

### Issue 5: "Port 5000 already in use"

**Solution:**

```bash
# Use different port
python -c "
from app import app
app.run(port=5001)
"
```

Or kill existing process:

```bash
# Windows
taskkill /PID <PORT_PID> /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

### Issue 6: "ImageMagick not found"

**Solution:** This is optional. If you need it:

**Windows:**

- Download: https://imagemagick.org/script/download.php#windows
- Install and add to PATH

**macOS:**

```bash
brew install imagemagick
```

**Linux:**

```bash
sudo apt-get install imagemagick
```

### Issue 7: "No medicines detected from image"

**Causes & Solutions:**

- Image quality too low → Use clearer image
- OCR isn't finding text → Try preprocessing
- Medicine names not recognized → Check supported medicines list

**Debug:**

```python
from ocr_module import PrescriptionOCR
ocr = PrescriptionOCR()
text = ocr.extract_text('prescription.jpg')
print("Extracted text:", text)
```

---

## 📊 Performance Verification

### Expected Performance

| Operation      | Time     | Accuracy |
| -------------- | -------- | -------- |
| Model Training | 1-5 min  | 92%      |
| Text Analysis  | <100ms   | >90%     |
| Image Analysis | 500ms-2s | >85%     |
| Prediction     | <50ms    | 92%      |

### System Requirements Met

- ✅ Python 3.8+ installed
- ✅ All dependencies installed
- ✅ Tesseract OCR working
- ✅ ML model trained
- ✅ Web server running
- ✅ API responding
- ✅ OCR functioning
- ✅ NLP working

---

## 🎓 Next Steps

1. **Explore Web Interface**
   - Upload sample prescription images
   - Test with different medicine combinations
   - View confidence scores

2. **Analyze Real Data**
   - Test with actual prescription images
   - Validate predictions
   - Collect feedback

3. **Customize System**
   - Add more medicines to `nlp_module.py`
   - Adjust ML model parameters in `config.py`
   - Improve OCR preprocessing

4. **Deploy to Production**
   - Move to production server
   - Enable HTTPS
   - Add authentication
   - Set up database

5. **Integrate with Hospital Systems**
   - API integration
   - Electronic health records (EHR)
   - Patient management systems

---

## 🎉 Success Checklist

- [ ] Python 3.8+ installed and verified
- [ ] All packages installed from requirements.txt
- [ ] Tesseract OCR installed and working
- [ ] spaCy model downloaded
- [ ] ML model trained successfully
- [ ] Demo script runs without errors
- [ ] Web application starts on localhost:5000
- [ ] Web interface loads in browser
- [ ] Can analyze text prescriptions
- [ ] Can analyze prescription images
- [ ] All modules respond within expected time
- [ ] Confidence scores are reasonable
- [ ] Risk levels are accurate

✅ **If all checkboxes are checked, you're ready to use PolypharmGuard!**

---

## 📞 Quick Support

| Problem          | Command                                       |
| ---------------- | --------------------------------------------- |
| Check Python     | `python --version`                            |
| Check packages   | `pip list`                                    |
| Verify Tesseract | `tesseract --version`                         |
| Test imports     | `python -c "import pandas, sklearn, xgboost"` |
| Train model      | `python train_model.py`                       |
| Run tests        | `python demo.py`                              |
| Start web app    | `python app.py`                               |
| Activate venv    | `venv\Scripts\activate` (Windows)             |
| Deactivate venv  | `deactivate`                                  |

---

## 📚 Documentation

- **README.md** - Full documentation
- **QUICKSTART.md** - 5-minute setup
- **This file** - Installation & testing guide
- **PROJECT_SUMMARY.md** - Project overview
- **Code comments** - Inline documentation

---

**Setup Complete! Ready to use PolypharmGuard** 🎊

Questions? Check the documentation files or review the code comments.

Happy drug interaction detection! 💊✨

---

Last Updated: 2024
Version: 1.0.0
