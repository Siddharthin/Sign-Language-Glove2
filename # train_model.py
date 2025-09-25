import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# 11 features + 1 label
columns = [
    'flex1', 'flex2', 'flex3', 'flex4', 'flex5',
    'acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z',
    'label'
]

# Load data and assign column names
df = pd.read_csv("gesture_data.csv", header=None)
df.columns = columns

# Split features and labels
X = df.drop("label", axis=1)
y = df["label"]

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "gesture_model.pkl")
print(" Model trained and saved as gesture_model.pkl")
