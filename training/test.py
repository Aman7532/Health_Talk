import os
import numpy as np
import pickle
import sys

def test_model():
    # Define symptoms list (should match what's in the app)
    print("Loading model test...")
    
    # Check if ExtraTrees model exists
    model_path = '../ExtraTrees'
    if not os.path.exists(model_path):
        print(f"Error: Model file '{model_path}' not found!")
        return False
        
    try:
        # Load the model
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        print("Model loaded successfully!")
        
        # Test with a sample input
        # Create a dummy symptom input (all zeros with a few symptoms set to 1)
        test_input = np.zeros(218)
        # Set a few random symptoms to 1 (e.g., cough, fever, headache positions)
        test_input[23] = 1  # cough 
        test_input[24] = 1  # high_fever
        test_input[30] = 1  # headache
        
        # Make a prediction
        prediction = model.predict([test_input])
        prediction_proba = model.predict_proba([test_input])
        top_indices = np.argsort(prediction_proba[0])[-3:][::-1]  # Top 3 classes
        
        print(f"Test prediction successful: {prediction}")
        print("Top 3 disease probabilities:")
        
        # Get a list of diseases (for display purposes only)
        # This should match the list in your main application
        diseases = [
            '(vertigo) Paroymsal  Positional Vertigo', 'AIDS', 'Acne', 'Alcoholic hepatitis', 'Allergy',
            'Arthritis', 'Bronchial Asthma', 'Cervical spondylosis', 'Chicken pox', 'Chronic cholestasis',
            'Common Cold', 'Dengue', 'Diabetes', 'Dimorphic hemmorhoids(piles)', 'Drug Reaction',
            'Fungal infection', 'GERD', 'Gastroenteritis', 'Heart attack', 'Hepatitis B', 'Hepatitis C',
            'Hepatitis D', 'Hepatitis E', 'Hypertension', 'Hyperthyroidism', 'Hypoglycemia', 'Hypothyroidism',
            'Impetigo', 'Jaundice', 'Malaria', 'Migraine', 'Osteoarthristis', 'Paralysis (brain hemorrhage)',
            'Peptic ulcer diseae', 'Pneumonia', 'Psoriasis', 'Tuberculosis', 'Typhoid',
            'Urinary tract infection', 'Varicose veins', 'hepatitis A'
        ]
        
        if len(diseases) > max(top_indices):
            for i in top_indices:
                print(f"- {diseases[i]}: {prediction_proba[0][i]:.4f}")
        else:
            print("Warning: Disease indices exceed the list length")
            
        return True
    except Exception as e:
        print(f"Error testing model: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_model()
    if not success:
        print("Model test failed!")
        sys.exit(1)
    else:
        print("Model test passed!")
        sys.exit(0) 