import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from satisfaction_analysis import calculate_engagement_score, calculate_experience_score


class TestSatisfactionAnalysis(unittest.TestCase):
    def test_engagement_score(self):
        user_data = [5, 10]
        cluster_center = [5, 5]
        self.assertAlmostEqual(calculate_engagement_score(user_data, cluster_center), 5.0)

    def test_experience_score(self):
        user_data = [1, 2]
        cluster_center = [2, 2]
        self.assertAlmostEqual(calculate_experience_score(user_data, cluster_center), 1.0)

if __name__ == '__main__':
    unittest.main()
