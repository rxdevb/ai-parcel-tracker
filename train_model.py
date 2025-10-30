import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import pickle
import datetime
import os
import sys
from typing import Dict, Any, Tuple

# Configuration Constants
RANDOM_STATE: int = 42
TEST_SIZE: float = 0.2
MODEL_FILENAME: str = 'model.pkl'
DATA_FILENAME: str = 'tracking_data.csv'


def load_data(filename: str) -> pd.DataFrame:
    """Loads training data from a CSV file."""
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        print(f"ERROR: Training data file '{filename}' not found. Cannot proceed.")
        sys.exit(1)


def preprocess_and_split(data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Applies feature engineering, encodes labels, and splits data for training."""

    # Use tracking number length as the primary feature.
    data['length'] = data['tracking_number'].apply(lambda x: len(str(x)))

    # Convert text labels (e.g., DPD) to numerical labels (0, 1, 2...).
    global le  # Must be accessible for saving to model.pkl
    le = LabelEncoder()
    data['label_encoded'] = le.fit_transform(data['label'])

    # Define features (X) and target (y)
    X = data[['length']]
    y = data['label_encoded']

    # Split data into training and testing sets (80/20) for validation.
    return train_test_split(X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE)


def train_and_evaluate(X_train: pd.DataFrame, X_test: pd.DataFrame, y_train: pd.Series, y_test: pd.Series) -> Tuple[
    DecisionTreeClassifier, float]:
    """Trains the model and calculates its test accuracy."""

    # Initialize and train the Decision Tree model.
    model = DecisionTreeClassifier(random_state=RANDOM_STATE)
    model.fit(X_train, y_train)

    # Evaluate performance on the test set.
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Test Accuracy: {accuracy:.4f}")

    return model, accuracy


def save_model(model: DecisionTreeClassifier, accuracy: float, features: list) -> None:
    """Serializes the model, encoder, and metadata to a file."""

    # Compile metadata for versioning and auditing.
    metadata: Dict[str, Any] = {
        'training_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'features': features,
        'model_type': 'DecisionTreeClassifier',
        'test_accuracy': accuracy
    }

    # Use 'le' from the global scope (defined in preprocess_and_split)
    with open(MODEL_FILENAME, 'wb') as file:
        pickle.dump({
            'model': model,
            'encoder': le,
            'metadata': metadata
        }, file)
    print(f"\nAI Model successfully saved to '{MODEL_FILENAME}'.")


if __name__ == '__main__':
    df = load_data(DATA_FILENAME)
    X_train, X_test, y_train, y_test = preprocess_and_split(df)
    trained_model, final_accuracy = train_and_evaluate(X_train, X_test, y_train, y_test)
    save_model(trained_model, final_accuracy, list(X_train.columns))