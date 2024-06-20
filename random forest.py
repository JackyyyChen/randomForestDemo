import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Load the data
file_path = 'multiple_regression_model_sampling_resullt.csv'
data = pd.read_csv(file_path)

# Prepare the data
X = data[['Linear', 'Digital']]
y = data['Overlap']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Regressor
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Predict using the test set
y_pred_rf = rf_model.predict(X_test)

# Evaluate the model
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

print(f'Mean Squared Error (MSE): {mse_rf}')
print(f'R-squared (R²): {r2_rf}')

# Function to make predictions
def predict_overlap(linear, digital):
    input_data = pd.DataFrame({'Linear': [linear], 'Digital': [digital]})
    overlap_prediction = rf_model.predict(input_data)[0]
    return overlap_prediction

# Example usage
linear_value = 10000000
digital_value = 10000000
predicted_overlap = predict_overlap(linear_value, digital_value)
print(f'Predicted Overlap: {predicted_overlap}')
