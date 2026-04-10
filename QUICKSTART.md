# PolypharmGuard Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Dependencies (2 minutes)

```bash
# Navigate to project directory
cd C:\Users\akhil\Desktop\polypharmguard

# Install Python packages
pip install -r requirements.txt
```

### Step 2: Install Tesseract OCR (1 minute)

**Windows:**

1. Download: https://github.com/UB-Mannheim/tesseract/wiki
2. Run installer and install to default location: `C:\Program Files\Tesseract-OCR`
3. Done!

**macOS/Linux:** See README.md

### Step 3: Download spaCy Model (1 minute)

```bash
python -m spacy download en_core_web_sm
```

### Step 4: Train the Model (1 minute)

```bash
python train_model.py
```

This will:

- Load the polypharmacy dataset (1,000 prescriptions)
- Train XGBoost model on drug combinations
- Save trained model to `models/` directory
- Display performance metrics

Expected output:

```
Model Accuracy: 0.9234
Confusion Matrix: [[...]]
...
✓ Model training completed successfully!
```

---

## 🌐 Launch Web Application

```bash
python app.py
```

Open browser: **http://localhost:5000**

### Web Interface Features:

- 📷 **Upload prescription image** - Automatic text extraction via OCR
- 📝 **Paste prescription text** - Direct text analysis
- 💊 **View extracted medicines**
- ⚠️ **Get risk level** - HIGH / MODERATE / LOW
- 📊 **See confidence score & probabilities**
- 📋 **Read detailed recommendations**

---

## 💻 Programmatic Usage

### Example 1: Analyze Text

```python
from polypharmguard import PolypharmGuard

guard = PolypharmGuard(model_trained=True)

prescription_text = """
Rx:
1. Ibuprofen 400 mg - twice daily
2. Warfarin 5 mg - once daily
3. Aspirin 75 mg - once daily
"""

result = guard.process_prescription_from_text(prescription_text)
print(guard.generate_report(result))
```

### Example 2: Analyze Image

```python
result = guard.process_prescription_from_image('prescription.jpg')
print(guard.generate_report(result))
```

### Example 3: Check Specific Medicines

```python
medicines = ['Ibuprofen', 'Warfarin', 'Aspirin']
result = guard.check_drug_interactions(medicines)

print(f"Risk Level: {result['risk_level']}")
print(f"Confidence: {result['confidence']}%")
```

---

## 🧪 Run Demo

See examples of all features:

```bash
python demo.py
```

This will show:

1. Text-based prescription analysis
2. Supported medicines list
3. Medicine detail extraction
4. Interaction checking on test cases

---

## 📂 Project Files Explained

| File                            | Purpose                                                |
| ------------------------------- | ------------------------------------------------------ |
| `ml_model.py`                   | ML model training, prediction, and feature engineering |
| `ocr_module.py`                 | OCR for extracting text from prescription images       |
| `nlp_module.py`                 | NLP for parsing medicine names, dosages, frequencies   |
| `polypharmguard.py`             | Main orchestrator combining ML, OCR, NLP               |
| `app.py`                        | Flask web application and REST API                     |
| `templates/index.html`          | Web UI interface                                       |
| `train_model.py`                | Standalone training script                             |
| `demo.py`                       | Interactive demonstrations                             |
| `polypharmacy_dataset_1000.csv` | Training dataset (1000 prescriptions)                  |

---

## ✅ Verification Checklist

After setup, verify everything works:

```bash
# 1. Check dependencies
python -c "import pandas, sklearn, xgboost, flask, spacy, nltk; print('✓ All packages installed')"

# 2. Test OCR
python -c "import pytesseract; print('✓ Tesseract available')"

# 3. Train model
python train_model.py

# 4. Run demo
python demo.py

# 5. Start web server
python app.py
# Then visit: http://localhost:5000
```

---

## 🎯 Common Tasks

### Task 1: Train with your own data

1. Replace `polypharmacy_dataset_1000.csv` with your dataset
2. Ensure CSV has columns: `Drugs`, `Risk_Level`
3. Run: `python train_model.py`

### Task 2: Add more medicines to detect

Edit `nlp_module.py`:

```python
MEDICINE_KEYWORDS = {
    'aspirin': ['aspirin', 'asa', 'bayer', 'YOUR_ALIAS'],
    'new_drug': ['new_drug', 'brand_name', 'another_name'],
    # ... add more
}
```

### Task 3: Analyze without web interface

```python
from polypharmguard import PolypharmGuard

guard = PolypharmGuard(model_trained=True)

# Text analysis
result = guard.process_prescription_from_text("Ibuprofen, Warfarin")
print(result)
```

---

## 🐛 Troubleshooting

### Issue: "Tesseract not found"

**Solution:**

```python
# In ocr_module.py, set path manually:
ocr = PrescriptionOCR(tesseract_path=r'C:\Program Files\Tesseract-OCR\tesseract.exe')
```

### Issue: "spaCy model not found"

**Solution:**

```bash
python -m spacy download en_core_web_sm
```

### Issue: "Model not trained"

**Solution:**

```bash
python train_model.py
```

### Issue: No medicines detected

- Ensure medicine name matches supported list
- Check `demo.py` to see supported medicines
- Text must have clear medicine names (not abbreviations)

---

## 📊 System Architecture

```
Prescription Input
       ↓
[OCR] Extract Text from Image OR [Direct Text Input]
       ↓
[NLP] Parse Medicine Names, Dosages, Frequencies
       ↓
[Drug Interaction Database] Estimate interaction counts
       ↓
[ML Model] Predict Risk Level (HIGH/MODERATE/LOW)
       ↓
[Report Generator] Create detailed recommendations
       ↓
Output: Risk Assessment + Recommendations
```

---

## 🎓 Learning Path

1. **Basic:** Run `demo.py` to understand system flow
2. **Intermediate:** Use web app to analyze prescriptions
3. **Advanced:** Modify `ml_model.py` to improve predictions
4. **Expert:** Integrate with drug interaction database APIs

---

## 📞 Quick Help

```bash
# View supported medicines
python -c "from polypharmguard import PolypharmGuard; g = PolypharmGuard(model_trained=True); print(list(g.nlp.MEDICINE_KEYWORDS.keys()))"

# Check model accuracy
python -c "from ml_model import DrugInteractionModel; m = DrugInteractionModel(); m.load_model(); print('✓ Model loaded')"

# Test NLP extraction
python -c "from nlp_module import MedicineNLP; nlp = MedicineNLP(); print(nlp.extract_medicines('Take 500mg Ibuprofen twice daily'))"
```

---

## 🎉 You're Ready!

Start with:

```bash
python app.py
```

Then open: **http://localhost:5000**

Enjoy using PolypharmGuard! 💊✨

---

**Need help?** Check README.md for detailed documentation.
