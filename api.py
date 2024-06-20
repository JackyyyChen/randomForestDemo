import pandas as pd
from flask import Flask, request, jsonify, send_from_directory
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Load and prepare the data
file_path = 'Overlap-NSW-Jan.csv'
data = pd.read_csv(file_path)

X = data[['Linear', 'Digital']]
y = data['Overlap']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Regressor
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Evaluate the model
y_pred_rf = rf_model.predict(X_test)
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

print(f'Mean Squared Error (MSE): {mse_rf}')
print(f'R-squared (R²): {r2_rf}')

# Initialize Flask app
app = Flask(__name__, static_url_path='')

# Define a route for prediction
@app.route('/predict', methods=['POST'])
def predict_overlap():
    # Get the request data
    data = request.get_json()
    try:
        linear = data['Linear']
        digital = data['Digital']
    except KeyError:
        return jsonify({"error": "Invalid input. Please provide 'Linear' and 'Digital' values."}), 400

    try:
        input_data = pd.DataFrame({'Linear': [linear], 'Digital': [digital]})
        overlap_prediction = rf_model.predict(input_data)[0]
        return jsonify({'Predicted Overlap': overlap_prediction})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Serve the static HTML file
@app.route('/')
def home():
    return send_from_directory('Front_end', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
