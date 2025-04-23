import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier

# Define the diseases and symptoms (same as in chatpdf1.py)
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

symptoms = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain',
          'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition',
          'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness',
          'lethargy', 'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes',
          'breathlessness', 'sweating', 'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine',
          'nausea', 'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain', 'constipation', 'abdominal_pain',
          'diarrhoea', 'mild_fever', 'yellow_urine', 'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload',
          'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm',
          'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain',
          'weakness_in_limbs', 'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region',
          'bloody_stool', 'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity',
          'swollen_legs', 'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails',
          'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips',
          'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints',
          'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side',
          'loss_of_smell', 'bladder_discomfort', 'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching',
          'toxic_look_(typhos)', 'depression', 'irritability', 'muscle_pain', 'altered_sensorium',
          'red_spots_over_body', 'belly_pain', 'abnormal_menstruation', 'watering_from_eyes', 'increased_appetite',
          'polyuria', 'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration',
          'visual_disturbances', 'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma',
          'stomach_bleeding', 'distention_of_abdomen', 'history_of_alcohol_consumption', 'blood_in_sputum',
          'prominent_veins_on_calf', 'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads',
          'scurring', 'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails',
          'blister', 'red_sore_around_nose', 'yellow_crust_ooze']

print(f"Number of symptoms: {len(symptoms)}")

# Let's check the number of features the chatpdf1.py is expecting
with open('chatpdf1.py', 'r') as f:
    content = f.read()
    
# Look for "features = [0] * 218" line in the code
import re
feature_count_match = re.search(r'features\s*=\s*\[0\]\s*\*\s*(\d+)', content)
if feature_count_match:
    expected_feature_count = int(feature_count_match.group(1))
    print(f"Expected feature count in chatpdf1.py: {expected_feature_count}")
else:
    expected_feature_count = 218
    print(f"Could not detect feature count, using default: {expected_feature_count}")

# Generate some sample data for training
def generate_training_data():
    # This is a simplified version for demonstration
    # In a real scenario, you'd use actual medical data
    n_samples = 1000
    X = np.zeros((n_samples, expected_feature_count))
    y = np.random.randint(0, len(diseases), n_samples)
    
    # For each sample, randomly activate some symptoms
    for i in range(n_samples):
        # Each disease has some specific symptoms
        disease_idx = y[i]
        # Activate 3-7 random symptoms
        n_active = np.random.randint(3, 8)
        # Make sure we're not exceeding the actual symptoms list length
        max_idx = min(len(symptoms), expected_feature_count)
        active_indices = np.random.choice(max_idx, n_active, replace=False)
        X[i, active_indices] = 1
    
    return X, y

print("Generating training data...")
X, y = generate_training_data()
print(f"Training data shape: X: {X.shape}, y: {y.shape}")

# Train the ExtraTreesClassifier
print("Training ExtraTreesClassifier...")
model = ExtraTreesClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save the model
print("Saving model to ExtraTrees...")
with open('ExtraTrees', 'wb') as f:
    pickle.dump(model, f)

print("Done! ExtraTrees model has been trained and saved.") 