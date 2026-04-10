#!/usr/bin/env python
"""
Training script for PolypharmGuard ML Model
Run this script once to train the model on the dataset
"""

from ml_model import DrugInteractionModel

def main():
    print("="*70)
    print("PolypharmGuard - ML Model Training Script")
    print("="*70)
    
    # Initialize model
    model = DrugInteractionModel()
    model.create_directories()
    
    # Load dataset
    print("\n[1/4] Loading dataset...")
    df = model.load_data('polypharmacy_dataset_1000.csv')
    
    # Preprocess data
    print("\n[2/4] Preprocessing data and extracting features...")
    X, y_encoded, y = model.preprocess_data(df)
    
    # Train model
    print("\n[3/4] Training XGBoost model...")
    X_test, y_test, y_pred = model.train_model(X, y_encoded)
    
    # Save model
    print("\n[4/4] Saving model and encoders...")
    model.save_model()
    
    print("\n" + "="*70)
    print("✓ Model training completed successfully!")
    print("="*70)
    print("\nModel files saved:")
    print(f"  - {model.model_path}")
    print(f"  - {model.drug_encoder_path}")
    print(f"  - {model.label_encoder_path}")
    print("\nYou can now run: python app.py")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
