import random
import numpy as np
import matplotlib.pyplot as plt

# Payoff matrix: (R, S, T, P)
R, S, T, P = 3, 0, 5, 1

# TFT Strategy
class TFT:
    def __init__(self):
        self.last = 'C'
    def move(self, opp_last):
        if opp_last is None:
            return 'C'
        return opp_last

# NAFT Strategy (simplified from canvas logic)
class NAFT:
    def __init__(self):
        self.defect_streak = 0
    def move(self, prev_state):
        if prev_state in ('CC', 'DC'):
            self.defect_streak = 0
        if prev_state in ('CD', 'DD'):
            self.defect_streak += 1
        
        if self.defect_streak >= 2:
            return 'D'
        
        mapping = {
            'CC': 1.0,
            'CD': 0.6,
            'DC': 1.0,
            'DD': 0.3
        }
        return 'C' if random.random() < mapping[prev_state] else 'D'

def play_round(a, b, noise=0.0):
    prev_state = 'CC'
    score_a = score_b = 0
    
    for _ in range(200):
        move_a = a.move(prev_state if isinstance(a, NAFT) else prev_state[1] if prev_state else None)
        move_b = b.move(prev_state if isinstance(b, NAFT) else prev_state[0] if prev_state else None)
        
        # Noise flips action
        if random.random() < noise:
            move_a = 'D' if move_a == 'C' else 'C'
        if random.random() < noise:
            move_b = 'D' if move_b == 'C' else 'C'
        
        if move_a == 'C' and move_b == 'C':
            score_a += R; score_b += R
        elif move_a == 'C' and move_b == 'D':
            score_a += S; score_b += T
        elif move_a == 'D' and move_b == 'C':
            score_a += T; score_b += S
        else:
            score_a += P; score_b += P
        
        prev_state = move_a + move_b
    
    return score_a/200, score_b/200

# Run sweep
noise_levels = np.linspace(0, 0.3, 15)
naft_scores = []
tft_scores = []

for n in noise_levels:
    na, tf = [], []
    for _ in range(100):
        a, b = NAFT(), TFT()
        sa, sb = play_round(a, b, noise=n)
        na.append(sa)
        tf.append(sb)
    naft_scores.append(np.mean(na))
    tft_scores.append(np.mean(tf))

# Plot
plt.figure()
plt.plot(noise_levels, naft_scores)
plt.plot(noise_levels, tft_scores)
plt.xlabel("Noise Level")
plt.ylabel("Average Payoff per Round")
plt.title("NAFT vs TFT Performance Under Noise")
plt.show()
