import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load the data
df = pd.read_csv('../../data/flights.csv')

# Feature engineering
df['DayOfWeek'] = df['DayOfWeek'].astype('category')
features = ['DayOfWeek', 'DestAirportID']
target = 'ArrDel15'

# Prepare features
X = pd.get_dummies(df[features], columns=['DayOfWeek'])
y = df[target]

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Save the model and scaler
with open('../backend/model.pkl', 'wb') as f:
    pickle.dump((model, scaler), f)

# Create airport lookup
airports = df[['DestAirportID', 'DestAirportName']].drop_duplicates()
airports.to_csv('../backend/airports.csv', index=False)

print("Model training completed and saved")
print(f"Model accuracy: {model.score(X_test_scaled, y_test):.2f}")