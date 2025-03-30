import numpy as np
from scipy.stats import beta


class Bandit:
    def __init__(self, n_arms: int):
        self.n_arms = n_arms
        self.engagements = np.zeros((n_arms, 2))
        self.impressions = np.zeros(n_arms)

    def pull(self, return_probs=False):
        samples = [self.beta(i) for i in range(self.n_arms)]
        best_arm = np.argmax(samples)

        self.impressions[best_arm] += 1

        if return_probs:
            return best_arm, samples

        return best_arm

    def beta(self, arm: int):
        s, f = self.engagements[arm]
        i = self.impressions[arm] / 10  # Add penalty to impressions.
        print(s, f, i)

        return np.random.beta(s + i + 1, f + i + 1)

    def beta_pdf(self, x, arm: int):
        s, f = self.engagements[arm]
        i = self.impressions[arm] / 10

        return beta.pdf(x, s + i + 1, f + i + 1)

    def update(self, arm: int, reward: bool):
        if reward:
            self.engagements[arm][0] += 1
        else:
            self.engagements[arm][1] += 1
