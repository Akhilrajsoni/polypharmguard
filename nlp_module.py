import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
import re
import spacy

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')


class MedicineNLP:
    """NLP module to extract medicine names and dosages from text"""
    
    # Common medicine patterns and synonyms
    MEDICINE_KEYWORDS = {
        'ibuprofen': ['ibuprofen', 'advil', 'motrin', 'brufen'],
        'paracetamol': ['paracetamol', 'acetaminophen', 'tylenol', 'calpol'],
        'aspirin': ['aspirin', 'asa', 'bayer'],
        'warfarin': ['warfarin', 'coumadin'],
        'tramadol': ['tramadol', 'ultram', 'tramal'],
        'fluoxetine': ['fluoxetine', 'prozac', 'sarafem'],
        'omeprazole': ['omeprazole', 'prilosec', 'losec'],
        'metformin': ['metformin', 'glucophage', 'fortamet'],
        'simvastatin': ['simvastatin', 'zocor'],
        'atorvastatin': ['atorvastatin', 'lipitor'],
        'lisinopril': ['lisinopril', 'prinivil', 'zestril'],
        'ramipril': ['ramipril', 'altace'],
        'losartan': ['losartan', 'cozaar'],
        'amlodipine': ['amlodipine', 'norvasc'],
        'furosemide': ['furosemide', 'lasix'],
        'insulin': ['insulin', 'lantus', 'humalog'],
        'prednisone': ['prednisone', 'deltasone'],
        'ciprofloxacin': ['ciprofloxacin', 'cipro'],
        'erythromycin': ['erythromycin', 'eryc'],
        'amiodarone': ['amiodarone', 'cordarone'],
        'diazepam': ['diazepam', 'valium'],
        'alprazolam': ['alprazolam', 'xanax'],
        'zolpidem': ['zolpidem', 'ambien'],
        'clopidogrel': ['clopidogrel', 'plavix', 'nprasugrel'],
    }
    
    # Dosage units
    DOSAGE_UNITS = ['mg', 'g', 'mcg', 'μg', 'ml', 'l', 'unit', 'units', 'iu', 'tablet', 'capsule', 'drop', 'spray']
    
    def __init__(self):
        """Initialize NLP module"""
        self.stop_words = set(stopwords.words('english'))
        
        # Additional medical stop words
        self.medical_stop_words = {'medicine', 'drug', 'tablet', 'medication', 'take', 'dose', 'use'}
        self.stop_words.update(self.medical_stop_words)
        
        # Load spaCy model for better NLP
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except OSError:
            print("Downloading spaCy model...")
            import os
            os.system('python -m spacy download en_core_web_sm')
            self.nlp = spacy.load('en_core_web_sm')
    
    def normalize_text(self, text):
        """Normalize text for processing"""
        text = text.lower().strip()
        text = re.sub(r'[^\w\s\-\(\),.]', '', text)  # Remove special characters
        return text
    
    def extract_medicines(self, text):
        """Extract medicine names from text using multiple methods"""
        normalized_text = self.normalize_text(text)
        
        found_medicines = set()
        
        # Method 1: Direct keyword matching
        for standard_name, synonyms in self.MEDICINE_KEYWORDS.items():
            for synonym in synonyms:
                if re.search(r'\b' + synonym + r'\b', normalized_text):
                    found_medicines.add(standard_name)
        
        # Method 2: NER with spaCy (if available)
        try:
            doc = self.nlp(text)
            for ent in doc.ents:
                if ent.label_ in ['GPE', 'PRODUCT', 'ORG']:  # Broad categories
                    entity_lower = ent.text.lower()
                    for standard_name, synonyms in self.MEDICINE_KEYWORDS.items():
                        if entity_lower in synonyms or standard_name in entity_lower:
                            found_medicines.add(standard_name)
        except Exception as e:
            print(f"SpaCy NER warning: {e}")
        
        # Method 3: Capitalized words (potential drug names)
        words = text.split()
        for word in words:
            cleaned_word = re.sub(r'[^\w]', '', word).lower()
            for standard_name, synonyms in self.MEDICINE_KEYWORDS.items():
                if cleaned_word in synonyms:
                    found_medicines.add(standard_name)
        
        return list(found_medicines)
    
    def extract_dosages(self, text):
        """Extract dosage information from text"""
        normalized_text = self.normalize_text(text)
        
        dosage_pattern = r'(\d+(?:\.\d+)?)\s*(' + '|'.join(self.DOSAGE_UNITS) + r')'
        matches = re.finditer(dosage_pattern, normalized_text, re.IGNORECASE)
        
        dosages = []
        for match in matches:
            dosages.append({
                'amount': float(match.group(1)),
                'unit': match.group(2).lower(),
                'full_text': match.group(0)
            })
        
        return dosages
    
    def extract_frequency(self, text):
        """Extract medication frequency from text"""
        normalized_text = self.normalize_text(text)
        
        frequencies = {
            'once daily': ['once daily', '1 time daily', '1x daily', 'od', 'once a day'],
            'twice daily': ['twice daily', '2 times daily', '2x daily', 'bid', 'bd'],
            'three times daily': ['three times daily', '3 times daily', '3x daily', 'tid', 'tds'],
            'four times daily': ['four times daily', '4 times daily', '4x daily', 'qid'],
            'weekly': ['once weekly', '1x weekly', 'weekly'],
            'every 6 hours': ['every 6 hours', 'q6h'],
            'every 8 hours': ['every 8 hours', 'q8h'],
            'every 12 hours': ['every 12 hours', 'q12h'],
        }
        
        found_frequencies = []
        for freq_name, keywords in frequencies.items():
            for keyword in keywords:
                if keyword in normalized_text:
                    found_frequencies.append(freq_name)
                    break
        
        return found_frequencies
    
    def parse_prescription_text(self, text):
        """Parse complete prescription text and extract structured information"""
        sentences = sent_tokenize(text)
        
        medicines_found = set()
        dosages = []
        frequencies = []
        
        for sentence in sentences:
            medicines_found.update(self.extract_medicines(sentence))
            dosages.extend(self.extract_dosages(sentence))
            frequencies.extend(self.extract_frequency(sentence))
        
        return {
            'medicines': list(medicines_found),
            'dosages': dosages,
            'frequencies': list(set(frequencies)),
            'raw_text': text
        }


def main():
    """Test NLP functionality"""
    nlp = MedicineNLP()
    
    # Test with sample prescription text
    sample_text = """
    Rx:
    1. Ibuprofen 400 mg - twice daily
    2. Warfarin 5 mg - once daily
    3. Aspirin 75 mg - once daily
    Take with food. Avoid dairy products with these medications.
    """
    
    result = nlp.parse_prescription_text(sample_text)
    print("Extracted Information:")
    print(f"Medicines: {result['medicines']}")
    print(f"Dosages: {result['dosages']}")
    print(f"Frequencies: {result['frequencies']}")


if __name__ == "__main__":
    main()
