import pandas as pd
from src.satisfaction_analysis import (
    calculate_engagement_score,
    calculate_experience_score,
    calculate_satisfaction_score
)

def compute_scores(data, least_engaged_center, worst_experience_center):
    data["engagement_score"] = data["user_data"].apply(
        lambda x: calculate_engagement_score(np.array(x), np.array(least_engaged_center))
    )
    data["experience_score"] = data["user_data"].apply(
        lambda x: calculate_experience_score(np.array(x), np.array(worst_experience_center))
    )
    data["satisfaction_score"] = data.apply(
        lambda row: calculate_satisfaction_score(row["engagement_score"], row["experience_score"]), axis=1
    )
    return data

def get_top_customers(data, n=10):
    return data.sort_values("satisfaction_score", ascending=False).head(n)

# Example usage
if __name__ == "__main__":
    data = pd.DataFrame({
        "user_id": [1, 2, 3],
        "user_data": [[5, 10], [3, 8], [7, 7]]
    })
    least_engaged_center = [0, 0]
    worst_experience_center = [10, 10]

    scored_data = compute_scores(data, least_engaged_center, worst_experience_center)
    top_customers = get_top_customers(scored_data)

    print(top_customers)
