import pandas as pd
import os
import platform
from ml_model import DrugInteractionModel
from ocr_module import PrescriptionOCR
from nlp_module import MedicineNLP


class PolypharmGuard:
    """Main PolypharmGuard system integrating ML, OCR, and NLP"""
    
    @staticmethod
    def _get_tesseract_path():
        """Detect Tesseract installation path"""
        if platform.system() == 'Windows':
            # Common Windows installation paths
            common_paths = [
                r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            ]
            for path in common_paths:
                if os.path.exists(path):
                    return path
        else:
            # Unix-like systems (Linux, macOS)
            # pytesseract will find it automatically via PATH
            pass
        return None
    
    def __init__(self, model_trained=False):
        """Initialize PolypharmGuard system"""
        self.ml_model = DrugInteractionModel()
        
        # Initialize OCR with Tesseract path if available
        tesseract_path = self._get_tesseract_path()
        if tesseract_path:
            self.ocr = PrescriptionOCR(tesseract_path=tesseract_path)
            print(f"✓ Tesseract OCR found at: {tesseract_path}")
        else:
            self.ocr = PrescriptionOCR()
            if platform.system() == 'Windows':
                print("⚠ Warning: Tesseract OCR not found. Install from: https://github.com/UB-Mannheim/tesseract/wiki")
        
        self.nlp = MedicineNLP()
        
        if model_trained:
            try:
                self.ml_model.load_model()
                print("ML model loaded successfully")
            except:
                print("ML model not found. Train the model first using train_model()")
    
    def train_model(self, dataset_path):
        """Train the drug interaction model"""
        print("Starting model training...")
        df = self.ml_model.load_data(dataset_path)
        X, y_encoded, y = self.ml_model.preprocess_data(df)
        X_test, y_test, y_pred = self.ml_model.train_model(X, y_encoded)
        self.ml_model.save_model()
        print("Model training completed!")
    
    def analyze_prescription_image(self, image_path):
        """Analyze a prescription image and extract medicines"""
        print(f"\nAnalyzing prescription image: {image_path}")
        
        # Extract text from image
        text = self.ocr.extract_text(image_path, preprocess=True)
        print(f"\nExtracted Text:\n{text}\n")
        
        # Parse extracted text
        prescription_data = self.nlp.parse_prescription_text(text)
        
        return prescription_data
    
    def analyze_prescription_text(self, text):
        """Analyze prescription text and extract medicines"""
        print(f"\nAnalyzing prescription text...")
        prescription_data = self.nlp.parse_prescription_text(text)
        return prescription_data
    
    def check_drug_interactions(self, medicines):
        """Check for drug interactions among given medicines"""
        print(f"\n{'='*60}")
        print(f"Checking interactions for: {medicines}")
        print(f"{'='*60}")
        
        # Count interactions (simplified - in production, use a drug interaction database)
        num_pairs = len(medicines) * (len(medicines) - 1) // 2
        
        # Estimate interaction counts (these should ideally come from a medical database)
        interaction_counts = {
            'total': num_pairs,
            'major': max(0, num_pairs - 2),
            'moderate': 1 if num_pairs > 0 else 0,
            'minor': 0
        }
        
        # Get prediction from ML model
        risk_level, confidence, probabilities = self.ml_model.predict(medicines, interaction_counts)
        
        print(f"\nDrugs Analyzed: {len(medicines)}")
        print(f"Number of Potential Drug Pairs: {num_pairs}")
        print(f"\nPredicted Risk Level: {risk_level}")
        print(f"Confidence: {confidence:.2f}%")
        print(f"\nRisk Probability Distribution:")
        for risk_type, prob in probabilities.items():
            print(f"  {risk_type}: {prob:.2f}%")
        
        return {
            'medicines': medicines,
            'num_drugs': len(medicines),
            'potential_pairs': num_pairs,
            'risk_level': risk_level,
            'confidence': confidence,
            'probabilities': probabilities
        }
    
    def process_prescription_from_image(self, image_path):
        """End-to-end: Process image -> Extract medicines -> Check interactions"""
        print(f"\n{'='*60}")
        print(f"PROCESSING PRESCRIPTION IMAGE")
        print(f"{'='*60}")
        
        # Step 1: Extract text from image
        prescription_data = self.analyze_prescription_image(image_path)
        medicines = prescription_data['medicines']
        
        if not medicines:
            print("\nWarning: No medicines could be extracted from the image.")
            return None
        
        print(f"\nExtracted Medicines: {medicines}")
        
        # Step 2: Check for interactions
        result = self.check_drug_interactions(medicines)
        
        # Add additional information
        result['dosages'] = prescription_data['dosages']
        result['frequencies'] = prescription_data['frequencies']
        
        return result
    
    def process_prescription_from_text(self, text):
        """End-to-end: Process text -> Extract medicines -> Check interactions"""
        print(f"\n{'='*60}")
        print(f"PROCESSING PRESCRIPTION TEXT")
        print(f"{'='*60}")
        
        # Step 1: Extract information from text
        prescription_data = self.analyze_prescription_text(text)
        medicines = prescription_data['medicines']
        
        if not medicines:
            print("\nWarning: No medicines could be extracted from the text.")
            return None
        
        print(f"\nExtracted Medicines: {medicines}")
        
        # Step 2: Check for interactions
        result = self.check_drug_interactions(medicines)
        
        # Add additional information
        result['dosages'] = prescription_data['dosages']
        result['frequencies'] = prescription_data['frequencies']
        
        return result
    
    def generate_report(self, analysis_result):
        """Generate a detailed report from analysis results"""
        if not analysis_result:
            return "No analysis results to report."
        
        report = f"""
{'='*60}
POLYPHARMACY INTERACTION ANALYSIS REPORT
{'='*60}

PRESCRIPTION DETAILS:
  Number of Medicines: {analysis_result['num_drugs']}
  Medicines: {', '.join(analysis_result['medicines'])}
  
INTERACTION ANALYSIS:
  Potential Drug Pairs: {analysis_result['potential_pairs']}
  
{("DOSAGES:" if analysis_result['dosages'] else "  No dosage information extracted")}
{(chr(10).join([f"    {d}" for d in analysis_result['dosages']]) if analysis_result['dosages'] else "")}
  
{("FREQUENCIES:" if analysis_result['frequencies'] else "  No frequency information extracted")}
{(chr(10).join([f"    {f}" for f in analysis_result['frequencies']]) if analysis_result['frequencies'] else "")}

RISK ASSESSMENT:
  Predicted Risk Level: {analysis_result['risk_level']}
  Confidence Score: {analysis_result['confidence']:.2f}%
  
PROBABILITY DISTRIBUTION:
"""
        for risk_type, prob in analysis_result['probabilities'].items():
            report += f"  {risk_type}: {prob:.2f}%\n"
        
        # Add recommendations based on risk level
        report += f"\nRECOMMENDATIONS:\n"
        if analysis_result['risk_level'] == 'HIGH':
            report += """  ⚠️  HIGH RISK COMBINATION DETECTED
  - Immediate consultation with pharmacist recommended
  - Consider alternative medications if possible
  - Monitor closely for adverse effects
  - Review each interaction individually
"""
        elif analysis_result['risk_level'] == 'MODERATE':
            report += """  ⚠️  MODERATE RISK COMBINATION
  - Consultation with healthcare provider recommended
  - Monitor for drug interactions
  - Adjust dosing if necessary
"""
        else:
            report += """  ✓ LOW RISK COMBINATION
  - Generally safe combination
  - Continue regular monitoring
  - Standard precautions apply
"""
        
        report += "\n" + "="*60 + "\n"
        return report


def main():
    """Example usage"""
    print("PolypharmGuard - Drug Interaction Detection System")
    print("="*60)
    
    # Initialize system
    guard = PolypharmGuard(model_trained=True)
    
    # Example 1: Analyze prescription text
    sample_prescription = """
    Patient: John Doe
    Date: 2024-01-15
    
    Rx:
    1. Ibuprofen 400 mg - twice daily for pain
    2. Warfarin 5 mg - once daily
    3. Aspirin 75 mg - once daily for heart health
    
    Instructions: Take medications with food.
    Do not take within 2 hours of dairy products.
    """
    
    result = guard.process_prescription_from_text(sample_prescription)
    if result:
        report = guard.generate_report(result)
        print(report)


if __name__ == "__main__":
    main()
