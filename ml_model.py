import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score
import joblib
import os

class DrugInteractionModel:
    """ML Model for detecting harmful drug interactions"""
    
    def __init__(self):
        self.model = None
        self.label_encoder = LabelEncoder()
        self.drug_encoder = {}
        self.feature_importance = None
        self.model_path = 'models/drug_interaction_model.pkl'
        self.drug_encoder_path = 'models/drug_encoder.pkl'
        self.label_encoder_path = 'models/label_encoder.pkl'
        
    def create_directories(self):
        """Create necessary directories"""
        os.makedirs('models', exist_ok=True)
        os.makedirs('results', exist_ok=True)
    
    def load_data(self, filepath):
        """Load the polypharmacy dataset"""
        df = pd.read_csv(filepath)
        print(f"Dataset shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        print(f"\nRisk Level Distribution:\n{df['Risk_Level'].value_counts()}")
        return df
    
    def extract_drug_features(self, drugs_str):
        """Extract features from drug list"""
        drugs = [drug.strip() for drug in drugs_str.split(',')]
        return drugs
    
    def preprocess_data(self, df):
        """Preprocess the dataset"""
        df_processed = df.copy()
        
        # Extract unique drugs from all prescriptions
        all_drugs = set()
        for drugs_str in df['Drugs']:
            drugs = self.extract_drug_features(drugs_str)
            all_drugs.update(drugs)
        
        print(f"\nTotal unique drugs: {len(all_drugs)}")
        self.drug_encoder = {drug: idx for idx, drug in enumerate(sorted(all_drugs))}
        
        # Create drug presence features
        drug_features = []
        for drugs_str in df['Drugs']:
            drugs = self.extract_drug_features(drugs_str)
            features = [1 if drug in drugs else 0 for drug in sorted(all_drugs)]
            drug_features.append(features)
        
        drug_feature_df = pd.DataFrame(
            drug_features,
            columns=[f'drug_{drug}' for drug in sorted(all_drugs)]
        )
        
        # Combine with other features
        feature_cols = ['Total_Drugs', 'DDI_Pairs_Count', 'Major_Interactions',
                       'Moderate_Interactions', 'Minor_Interactions']
        
        X = pd.concat([
            df_processed[feature_cols],
            drug_feature_df
        ], axis=1)
        
        y = df_processed['Risk_Level']
        y_encoded = self.label_encoder.fit_transform(y)
        
        print(f"\nFeature matrix shape: {X.shape}")
        print(f"Features include: {feature_cols} + {len(all_drugs)} drug features")
        
        return X, y_encoded, y
    
    def train_model(self, X, y_encoded):
        """Train the drug interaction detection model"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
        )
        
        # Train XGBoost model
        print("\nTraining XGBoost model...")
        self.model = XGBClassifier(
            n_estimators=200,
            max_depth=8,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            eval_metric='mlogloss'
        )
        
        self.model.fit(
            X_train, y_train,
            eval_set=[(X_test, y_test)],
            verbose=False
        )
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\nModel Accuracy: {accuracy:.4f}")
        print(f"\nClassification Report:")
        print(classification_report(
            y_test, y_pred,
            target_names=self.label_encoder.classes_
        ))
        
        return X_test, y_test, y_pred
    
    def save_model(self):
        """Save trained model and encoders"""
        self.create_directories()
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.drug_encoder, self.drug_encoder_path)
        joblib.dump(self.label_encoder, self.label_encoder_path)
        print(f"\nModel saved to {self.model_path}")
        print(f"Drug encoder saved to {self.drug_encoder_path}")
        print(f"Label encoder saved to {self.label_encoder_path}")
    
    def load_model(self):
        """Load trained model and encoders"""
        self.model = joblib.load(self.model_path)
        self.drug_encoder = joblib.load(self.drug_encoder_path)
        self.label_encoder = joblib.load(self.label_encoder_path)
        print("Model and encoders loaded successfully")
    
    def predict(self, drugs_list, interaction_counts):
        """
        Predict risk level for a drug combination
        
        Args:
            drugs_list: List of drug names
            interaction_counts: Dict with keys 'total', 'major', 'moderate', 'minor'
        
        Returns:
            risk_level: Predicted risk level (HIGH, MODERATE, LOW)
            confidence: Confidence score
        """
        if self.model is None:
            self.load_model()
        
        # Create feature vector
        feature_vector = []
        
        # Add basic features
        num_drugs = len(drugs_list)
        feature_vector.append(num_drugs)
        feature_vector.append(interaction_counts.get('total', 0))
        feature_vector.append(interaction_counts.get('major', 0))
        feature_vector.append(interaction_counts.get('moderate', 0))
        feature_vector.append(interaction_counts.get('minor', 0))
        
        # Add drug presence features
        for drug in sorted(self.drug_encoder.keys()):
            feature_vector.append(1 if drug in drugs_list else 0)
        
        X_pred = np.array([feature_vector])
        
        # Make prediction
        pred_class = self.model.predict(X_pred)[0]
        pred_proba = self.model.predict_proba(X_pred)[0]
        
        risk_level = self.label_encoder.inverse_transform([pred_class])[0]
        confidence = max(pred_proba) * 100
        
        return risk_level, confidence, dict(zip(self.label_encoder.classes_, pred_proba * 100))


def main():
    """Main training function"""
    model = DrugInteractionModel()
    model.create_directories()
    
    # Load and prepare data
    df = model.load_data('polypharmacy_dataset_1000.csv')
    X, y_encoded, y = model.preprocess_data(df)
    
    # Train model
    X_test, y_test, y_pred = model.train_model(X, y_encoded)
    
    # Save model
    model.save_model()
    
    # Test prediction
    print("\n" + "="*50)
    print("Testing prediction on sample drugs:")
    print("="*50)
    test_drugs = ['Ibuprofen', 'Warfarin', 'Aspirin']
    test_interactions = {'total': 3, 'major': 1, 'moderate': 1, 'minor': 1}
    risk, conf, probs = model.predict(test_drugs, test_interactions)
    print(f"Drugs: {test_drugs}")
    print(f"Predicted Risk Level: {risk}")
    print(f"Confidence: {conf:.2f}%")
    print(f"Probabilities: {probs}")


if __name__ == "__main__":
    main()
