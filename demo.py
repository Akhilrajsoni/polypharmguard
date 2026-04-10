#!/usr/bin/env python
"""
Demo script showing how to use PolypharmGuard programmatically
"""

from polypharmguard import PolypharmGuard

def demo_text_analysis():
    """Demo: Analyze prescription text"""
    print("\n" + "="*70)
    print("DEMO 1: Prescription Text Analysis")
    print("="*70)
    
    guard = PolypharmGuard(model_trained=True)
    
    sample_prescription = """
    Patient: John Doe
    Date: 2024-01-15
    
    Rx:
    1. Ibuprofen 400 mg - twice daily for pain
    2. Warfarin 5 mg - once daily for blood clotting
    3. Aspirin 75 mg - once daily for heart health
    
    Instructions: Take medications with food.
    Do not take within 2 hours of dairy products.
    """
    
    result = guard.process_prescription_from_text(sample_prescription)
    if result:
        report = guard.generate_report(result)
        print(report)


def demo_supported_medicines():
    """Demo: Show supported medicines"""
    print("\n" + "="*70)
    print("DEMO 2: Supported Medicines")
    print("="*70)
    
    guard = PolypharmGuard(model_trained=True)
    medicines = sorted(list(guard.nlp.MEDICINE_KEYWORDS.keys()))
    
    print(f"\nTotal supported medicines: {len(medicines)}\n")
    
    # Print in columns
    col_width = 20
    for i, medicine in enumerate(medicines, 1):
        print(f"{medicine:<{col_width}}", end="")
        if i % 3 == 0:
            print()
    print("\n")


def demo_extract_from_text():
    """Demo: Extract medicine details from text"""
    print("\n" + "="*70)
    print("DEMO 3: Extract Medicine Details")
    print("="*70)
    
    guard = PolypharmGuard(model_trained=True)
    
    text = """
    Take 500mg of Paracetamol three times daily with meals.
    Also take 200mg of Ibuprofen twice daily for inflammation.
    Fluoxetine 20mg once daily in the morning.
    """
    
    print(f"Input text:\n{text}\n")
    
    result = guard.nlp.parse_prescription_text(text)
    
    print(f"Extracted Medicines:")
    for medicine in result['medicines']:
        print(f"  - {medicine}")
    
    print(f"\nExtracted Dosages:")
    for dosage in result['dosages']:
        print(f"  - {dosage['amount']} {dosage['unit']}")
    
    print(f"\nExtracted Frequencies:")
    for freq in result['frequencies']:
        print(f"  - {freq}")


def demo_interaction_check():
    """Demo: Check specific drug interactions"""
    print("\n" + "="*70)
    print("DEMO 4: Drug Interaction Checking")
    print("="*70)
    
    guard = PolypharmGuard(model_trained=True)
    
    # Test case 1: High-risk combination
    print("\nTest Case 1: Potentially High-Risk Combination")
    medicines_1 = ['Warfarin', 'Ibuprofen', 'Aspirin', 'Simvastatin']
    result_1 = guard.check_drug_interactions(medicines_1)
    
    # Test case 2: Low-risk combination
    print("\n" + "-"*70)
    print("\nTest Case 2: Low-Risk Combination")
    medicines_2 = ['Metformin', 'Vitamin D']
    result_2 = guard.check_drug_interactions(medicines_2)
    
    # Test case 3: Moderate-risk combination
    print("\n" + "-"*70)
    print("\nTest Case 3: Moderate-Risk Combination")
    medicines_3 = ['Furosemide', 'Ramipril', 'Spironolactone']
    result_3 = guard.check_drug_interactions(medicines_3)


def main():
    """Run all demos"""
    print("\n" + "="*70)
    print("PolypharmGuard - Usage Demonstrations")
    print("="*70)
    
    try:
        demo_text_analysis()
        demo_supported_medicines()
        demo_extract_from_text()
        demo_interaction_check()
        
        print("\n" + "="*70)
        print("All demos completed successfully!")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\nError during demo: {e}")
        print("\nMake sure to run: python train_model.py first")


if __name__ == "__main__":
    main()
