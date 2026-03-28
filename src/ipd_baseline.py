#!/usr/bin/env python3
"""
ipd_baseline.py — Baseline IPD Evolutionary Dynamics (4-Strategy Population)
==============================================================================
A self-contained baseline simulation of evolutionary dynamics in the Iterated
Prisoner's Dilemma without NAFT. Used to establish a comparison point for
classical strategy behavior under noise.

Strategy pool: AlwaysCooperate, AlwaysDefect, TitForTat, GrimTrigger.
Runs round-robin tournaments with fitness-proportional selection.
Noise levels tested: ε ∈ {0.0, 0.01, 0.05}.

Usage:
    python src/ipd_baseline.py
"""

import random
import numpy as np
import matplotlib.pyplot as plt

# =========================
# GLOBAL PARAMETERS
# =========================
ROUNDS = 150
POPULATION_SIZE = 120
GENERATIONS = 60
MUTATION_RATE = 0.02
EPSILON_VALUES = [0.0, 0.01, 0.05]

# Prisoner's Dilemma Payoff Matrix
PAYOFFS = {
    ('C', 'C'): (3, 3),
    ('C', 'D'): (0, 5),
    ('D', 'C'): (5, 0),
    ('D', 'D'): (1, 1)
}

# =========================
# STRATEGIES
# =========================
class Strategy:
    def reset(self):
        pass

    def move(self, opponent_last):
        pass


class AlwaysCooperate(Strategy):
    def move(self, opponent_last):
        return 'C'


class AlwaysDefect(Strategy):
    def move(self, opponent_last):
        return 'D'


class TitForTat(Strategy):
    def __init__(self):
        self.last_opponent = 'C'

    def reset(self):
        self.last_opponent = 'C'

    def move(self, opponent_last):
        return opponent_last if opponent_last else 'C'


class GrimTrigger(Strategy):
    def __init__(self):
        self.triggered = False

    def reset(self):
        self.triggered = False

    def move(self, opponent_last):
        if opponent_last == 'D':
            self.triggered = True
        return 'D' if self.triggered else 'C'


STRATEGY_SET = [
    AlwaysCooperate,
    AlwaysDefect,
    TitForTat,
    GrimTrigger
]

# =========================
# CORE MATCH ENGINE
# =========================
def play_match(s1, s2, epsilon=0.0):
    s1.reset()
    s2.reset()

    last1, last2 = None, None
    score1, score2 = 0, 0

    for _ in range(ROUNDS):
        m1 = s1.move(last2)
        m2 = s2.move(last1)

        # Noise
        if random.random() < epsilon:
            m1 = 'D' if m1 == 'C' else 'C'
        if random.random() < epsilon:
            m2 = 'D' if m2 == 'C' else 'C'

        p1, p2 = PAYOFFS[(m1, m2)]
        score1 += p1
        score2 += p2

        last1, last2 = m1, m2

    return score1, score2


# =========================
# TOURNAMENT
# =========================
def run_tournament(population, epsilon):
    scores = np.zeros(len(population))

    for i in range(len(population)):
        for j in range(i + 1, len(population)):
            s1, s2 = population[i], population[j]
            sc1, sc2 = play_match(s1, s2, epsilon)
            scores[i] += sc1
            scores[j] += sc2

    return scores


# =========================
# EVOLUTIONARY DYNAMICS
# =========================
def evolve_population(population, scores):
    fitness = scores / scores.sum()
    new_population = []

    for _ in range(len(population)):
        parent = np.random.choice(population, p=fitness)
        if random.random() < MUTATION_RATE:
            new_population.append(random.choice(STRATEGY_SET)())
        else:
            new_population.append(type(parent)())

    return new_population


# =========================
# NOISE SWEEP EXPERIMENT
# =========================
def run_experiment(epsilon):
    population = [random.choice(STRATEGY_SET)() for _ in range(POPULATION_SIZE)]
    history = []

    for _ in range(GENERATIONS):
        scores = run_tournament(population, epsilon)
        counts = {
            'AC': sum(isinstance(p, AlwaysCooperate) for p in population),
            'AD': sum(isinstance(p, AlwaysDefect) for p in population),
            'TFT': sum(isinstance(p, TitForTat) for p in population),
            'GT': sum(isinstance(p, GrimTrigger) for p in population)
        }
        history.append(counts)
        population = evolve_population(population, scores)

    return history


# =========================
# MAIN + OPTIONAL PLOTTING
# =========================
if __name__ == "__main__":
    results = {}

    for eps in EPSILON_VALUES:
        print(f"Running simulation for epsilon = {eps}")
        results[eps] = run_experiment(eps)

    # ---- Plotting (optional but recommended) ----
    for eps, hist in results.items():
        ac = [h['AC'] for h in hist]
        ad = [h['AD'] for h in hist]
        tft = [h['TFT'] for h in hist]
        gt = [h['GT'] for h in hist]

        plt.figure()
        plt.plot(ac, label='Always Cooperate')
        plt.plot(ad, label='Always Defect')
        plt.plot(tft, label='Tit-for-Tat')
        plt.plot(gt, label='Grim Trigger')
        plt.title(f"Evolution of Strategies (ε = {eps})")
        plt.xlabel("Generation")
        plt.ylabel("Population Count")
        plt.legend()
        plt.show()
