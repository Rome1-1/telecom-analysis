from scipy.spatial import distance
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt


def calculate_engagement_score(user_data, cluster_center_of_least_engaged):
    return distance.euclidean(user_data, cluster_center_of_least_engaged)

def calculate_experience_score(user_data, worst_experience_cluster_center):
    return distance.euclidean(user_data, worst_experience_cluster_center)

def get_top_satisfied_customers(data):
    return data.sort_values(by="satisfaction_score", ascending=False).head(10)

def train_regression_model(data):
    X = data[["engagement_score", "experience_score"]]
    y = data["satisfaction_score"]

    # Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Evaluate Model
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print(f"Mean Squared Error: {mse}")
    return model

def perform_kmeans(data, n_clusters=2):
    X = data[["engagement_score", "experience_score"]]
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    data["cluster"] = kmeans.fit_predict(X)

    # Optional Plot
    plt.scatter(data["engagement_score"], data["experience_score"], c=data["cluster"], cmap="viridis")
    plt.title("K-Means Clustering")
    plt.xlabel("Engagement Score")
    plt.ylabel("Experience Score")
    plt.show()
    return data

def aggregate_scores_per_cluster(data):
    return data.groupby("cluster")[["satisfaction_score", "experience_score"]].mean()
