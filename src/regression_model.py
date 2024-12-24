from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def build_regression_model(data):
    X = data[['engagement_score', 'experience_score']]
    y = data['satisfaction_score']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    return model, y_pred
