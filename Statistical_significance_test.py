import random
import numpy as np
from scipy.stats import ttest_rel

R, S, T, P = 3, 0, 5, 1

class TFT:
    def move(self, opp_last):
        return 'C' if opp_last is None else opp_last

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
        mapping = {'CC':1.0,'CD':0.6,'DC':1.0,'DD':0.3}
        return 'C' if random.random() < mapping[prev_state] else 'D'

def play_match(a, b, noise=0.1, rounds=300):
    prev_state = 'CC'
    sa = sb = 0
    for _ in range(rounds):
        ma = a.move(prev_state if isinstance(a, NAFT) else prev_state[1])
        mb = b.move(prev_state if isinstance(b, NAFT) else prev_state[0])
        if random.random() < noise:
            ma = 'D' if ma == 'C' else 'C'
        if random.random() < noise:
            mb = 'D' if mb == 'C' else 'C'
        if ma=='C' and mb=='C':
            sa+=R; sb+=R
        elif ma=='C' and mb=='D':
            sa+=S; sb+=T
        elif ma=='D' and mb=='C':
            sa+=T; sb+=S
        else:
            sa+=P; sb+=P
        prev_state = ma+mb
    return sa/rounds, sb/rounds

noise = 0.15
trials = 400

naft_scores = []
tft_scores = []

for _ in range(trials):
    na, tf = play_match(NAFT(), TFT(), noise=noise)
    naft_scores.append(na)
    tft_scores.append(tf)

naft_scores = np.array(naft_scores)
tft_scores = np.array(tft_scores)

diff = naft_scores - tft_scores
mean_diff = diff.mean()
std_diff = diff.std(ddof=1)

t_stat, p_val = ttest_rel(naft_scores, tft_scores)

cohens_d = mean_diff / std_diff

mean_naft = naft_scores.mean()
mean_tft = tft_scores.mean()

mean_naft, mean_tft, mean_diff, t_stat, p_val, cohens_d
