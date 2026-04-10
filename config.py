# PolypharmGuard Configuration File

# =============================================================================
# OCR Configuration
# =============================================================================

# Path to Tesseract OCR executable
# Windows default: C:\Program Files\Tesseract-OCR\tesseract.exe
# macOS: /usr/local/bin/tesseract
# Linux: /usr/bin/tesseract
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# OCR Confidence threshold (0-100)
# Text with confidence below this will be filtered
OCR_CONFIDENCE_THRESHOLD = 30

# Image preprocessing settings
PREPROCESS_IMAGES = True
IMAGE_DENOISE_STRENGTH = 10

# =============================================================================
# NLP Configuration
# =============================================================================

# Supported medicine aliases
SUPPORTED_MEDICINES = {
    'ibuprofen': ['ibuprofen', 'advil', 'motrin', 'brufen'],
    'paracetamol': ['paracetamol', 'acetaminophen', 'tylenol', 'calpol'],
    'aspirin': ['aspirin', 'asa', 'bayer'],
    'warfarin': ['warfarin', 'coumadin'],
    'tramadol': ['tramadol', 'ultram', 'tramal'],
    'fluoxetine': ['fluoxetine', 'prozac', 'sarafem'],
    # Add more medicines here
}

# =============================================================================
# ML Model Configuration
# =============================================================================

# Model type
MODEL_TYPE = 'xgboost'  # Options: 'xgboost', 'randomforest'

# XGBoost parameters
XGBOOST_PARAMS = {
    'n_estimators': 200,
    'max_depth': 8,
    'learning_rate': 0.05,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'random_state': 42,
}

# Train/test split ratio
TEST_SIZE = 0.2
RANDOM_STATE = 42

# Model file paths
MODEL_PATH = 'models/drug_interaction_model.pkl'
DRUG_ENCODER_PATH = 'models/drug_encoder.pkl'
LABEL_ENCODER_PATH = 'models/label_encoder.pkl'

# =============================================================================
# Flask Web Application Configuration
# =============================================================================

# Flask settings
FLASK_ENV = 'development'  # Options: 'development', 'production'
FLASK_DEBUG = True
FLASK_PORT = 5000
FLASK_HOST = 'localhost'

# File upload settings
UPLOAD_FOLDER = 'uploads'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

# =============================================================================
# Dataset Configuration
# =============================================================================

# Path to training dataset
DATASET_PATH = 'polypharmacy_dataset_1000.csv'

# Dataset columns
DATASET_COLUMNS = {
    'case_id': 'Case_ID',
    'drugs': 'Drugs',
    'total_drugs': 'Total_Drugs',
    'ddi_pairs': 'DDI_Pairs_Count',
    'major_interactions': 'Major_Interactions',
    'moderate_interactions': 'Moderate_Interactions',
    'minor_interactions': 'Minor_Interactions',
    'risk_level': 'Risk_Level',
}

# =============================================================================
# System Settings
# =============================================================================

# Logging
LOGGING_LEVEL = 'INFO'  # Options: 'DEBUG', 'INFO', 'WARNING', 'ERROR'
LOG_FILE = 'polypharmguard.log'

# API settings
API_TIMEOUT = 30  # seconds
API_MAX_RETRIES = 3

# Risk level colors (for UI)
RISK_COLORS = {
    'HIGH': '#ff6b6b',
    'MODERATE': '#ffa500',
    'LOW': '#51cf66'
}

# =============================================================================
# Feature Engineering
# =============================================================================

# Feature extraction settings
USE_DRUG_PRESENCE = True  # Include binary drug presence features
USE_INTERACTION_COUNTS = True  # Include interaction count features
NORMALIZE_FEATURES = True  # Normalize feature values

# =============================================================================
# Prediction Settings
# =============================================================================

# Minimum confidence threshold for displaying predictions
MIN_CONFIDENCE_THRESHOLD = 0.5  # 50%

# Risk level thresholds (for boundary cases)
HIGH_RISK_THRESHOLD = 0.65
MODERATE_RISK_THRESHOLD = 0.35
# Anything below MODERATE_RISK_THRESHOLD is LOW_RISK

# =============================================================================
# Advanced Settings
# =============================================================================

# Enable experimental features
EXPERIMENTAL_FEATURES = False

# Cache predictions
ENABLE_PREDICTION_CACHE = True
CACHE_MAX_AGE = 3600  # seconds

# Enable GPU acceleration (if available)
USE_GPU = False

# =============================================================================
# Database Configuration (for future use)
# =============================================================================

# DATABASE_URL = 'postgresql://user:password@localhost:5432/polypharmguard'
# DATABASE_TYPE = 'postgresql'  # Options: 'postgresql', 'mysql', 'sqlite'

# =============================================================================
# End of Configuration
# =============================================================================
