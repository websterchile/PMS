#model training script on the dataset from temperature and vibrations sensors
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

def train_model(data_path):
    # Load the dataset
    data = pd.read_csv(data_path)

    # Preprocess the data
    # Assuming 'label' is the target variable and all other columns are features
    X = data.drop(columns=['label'])
    y = data['label']

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)

    # Train the model
    model.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Evaluate the model
    print(classification_report(y_test, y_pred))
    print(f"Accuracy: {accuracy_score(y_test, y_pred)}")

    # Save the trained model to a file
    joblib.dump(model, 'trained_model.pkl')