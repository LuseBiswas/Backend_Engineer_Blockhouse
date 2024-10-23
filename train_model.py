# train_model.py
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import joblib

# Sample function to generate and save a model
def train_model():
    # Load your historical stock data
    # For demonstration, we're creating a dummy DataFrame
    data = {
        'date': pd.date_range(start='2020-01-01', periods=100),
        'close_price': [i + (i * 0.1 * (0.5 - (i % 10) / 10.0)) for i in range(100)]
    }
    df = pd.DataFrame(data)

    # Prepare the data
    df['day'] = df['date'].dt.dayofyear
    X = df[['day']]
    y = df['close_price']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Save the model
    joblib.dump(model, 'model.pkl')

if __name__ == "__main__":
    train_model()
