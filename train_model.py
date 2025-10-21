import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

# 1. Load Data
data = pd.read_csv('tracking_data.csv')

# 2. Feature Engineering: Create features for the model
# We will use the length of the tracking number as the main feature
data['length'] = data['tracking_number'].apply(lambda x: len(str(x)))

# 3. Data Preprocessing
# Convert text labels (DPD, INPOST, etc.) to numbers
le = LabelEncoder()
data['label_encoded'] = le.fit_transform(data['label'])

X = data[['length']] # Features (input)
y = data['label_encoded'] # Target (output)

# 4. Train the AI Model (Decision Tree Classifier is simple and effective here)
model = DecisionTreeClassifier()
model.fit(X, y)

# 5. Save the trained model and the label encoder
with open('model.pkl', 'wb') as file:
    pickle.dump({'model': model, 'encoder': le}, file)

print("AI Model trained successfully and saved as model.pkl")