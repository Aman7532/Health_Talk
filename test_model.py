import pickle
import numpy as np

# Try to load the model
print("Loading the ExtraTrees model...")
try:
    with open('ExtraTrees', 'rb') as f:
        model = pickle.load(f)
    print("Model loaded successfully!")
    
    # Create a sample feature vector (218 features with all zeros except first two set to 1)
    features = [0] * 218
    features[0] = 1  # itching
    features[1] = 1  # skin_rash
    
    print(f"Feature vector shape: {len(features)}")
    print(f"First few elements: {features[:10]}")
    
    # Make a prediction
    print("Making a prediction...")
    try:
        proba = model.predict_proba([features])
        print(f"Prediction successful! Shape of probabilities: {proba.shape}")
        
        # Get top 5 predictions
        top5_idx = np.argsort(proba[0])[-5:][::-1]
        top5_proba = np.sort(proba[0])[-5:][::-1]
        
        # Define the diseases (same as in chatpdf1.py)
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
        
        # Get disease names for top predictions
        top5_diseases = [diseases[i] for i in top5_idx]
        
        print("\nTop 5 predictions:")
        for i in range(5):
            print(f"{i+1}. {top5_diseases[i]} - {top5_proba[i]:.2f}")
            
    except Exception as e:
        print(f"Error during prediction: {str(e)}")
        
except Exception as e:
    print(f"Error loading model: {str(e)}") 