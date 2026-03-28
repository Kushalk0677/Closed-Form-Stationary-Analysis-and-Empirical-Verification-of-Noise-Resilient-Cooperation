#!/usr/bin/env python3
"""
evolution.py — Evolutionary Multi-Strategy IPD Simulation
==========================================================
Corresponds to: Section 5.23–5.28 and Section 6.12–6.14 of the paper
(Evolutionary Multi-Strategy Robustness Experiment and Results).

Simulates a finite population of 300 agents across 200 generations.
Strategy pool: TFT, NAFT, WSLS, Grim Trigger, AllC, AllD, Random.
Fitness-proportional selection with mutation rate µ = 0.01.
Outputs: evolution_results.csv, phase_diagram.png, naft_survival.png,
         and per-epsilon strategy evolution plots.
"""

import numpy as np
import random
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing

# =========================
# GLOBAL PARAMETERS
# =========================

R, T, P, S = 3, 5, 1, 0
ROUNDS = 150
POP_SIZE = 300
GENERATIONS = 200
MATCHES_PER_AGENT = 8
MUTATION_RATE = 0.01
SEEDS = 30

NOISE_LEVELS = np.linspace(0.001, 0.3, 10)
NAFT_ALPHA = 0.2

MAX_WORKERS = 3  # Good for 4-core CPU

# =========================
# PAYOFF FUNCTION
# =========================

def payoff(a, b):
    if a == 'C' and b == 'C': return R
    if a == 'C' and b == 'D': return S
    if a == 'D' and b == 'C': return T
    return P

# =========================
# STRATEGIES
# =========================

class Strategy:
    def reset(self): pass
    def move(self, my_hist, opp_hist): raise NotImplementedError

class TFT(Strategy):
    def move(self, my_hist, opp_hist):
        return 'C' if len(opp_hist) == 0 else opp_hist[-1]

class AlwaysCooperate(Strategy):
    def move(self, *_): return 'C'

class AlwaysDefect(Strategy):
    def move(self, *_): return 'D'

class WSLS(Strategy):
    def move(self, my_hist, opp_hist):
        if len(my_hist) == 0: return 'C'
        last_my, last_opp = my_hist[-1], opp_hist[-1]
        return last_my if payoff(last_my, last_opp) >= R else ('D' if last_my == 'C' else 'C')

class GrimTrigger(Strategy):
    def __init__(self): self.grim = False
    def reset(self): self.grim = False
    def move(self, my_hist, opp_hist):
        if 'D' in opp_hist: self.grim = True
        return 'D' if self.grim else 'C'

class RandomStrategy(Strategy):
    def move(self, *_): return random.choice(['C', 'D'])

class NAFT(Strategy):
    def __init__(self, alpha=NAFT_ALPHA): self.alpha = alpha
    def move(self, my_hist, opp_hist):
        if len(opp_hist) == 0: return 'C'
        if opp_hist[-1] == 'D':
            return 'C' if random.random() < self.alpha else 'D'
        return 'C'

# =========================
# NOISE
# =========================

def apply_noise(action, epsilon):
    if random.random() < epsilon:
        return 'D' if action == 'C' else 'C'
    return action

# =========================
# MATCH
# =========================

def play_match(s1, s2, epsilon):

    s1.reset()
    s2.reset()

    h1, h2 = [], []
    sc1 = sc2 = 0

    for _ in range(ROUNDS):

        m1 = apply_noise(s1.move(h1, h2), epsilon)
        m2 = apply_noise(s2.move(h2, h1), epsilon)

        sc1 += payoff(m1, m2)
        sc2 += payoff(m2, m1)

        h1.append(m1)
        h2.append(m2)

    return sc1 / ROUNDS, sc2 / ROUNDS

# =========================
# POPULATION
# =========================

POOL = {
    "TFT": TFT,
    "NAFT": NAFT,
    "WSLS": WSLS,
    "Grim": GrimTrigger,
    "AllC": AlwaysCooperate,
    "AllD": AlwaysDefect,
    "Random": RandomStrategy
}

POOL_KEYS = list(POOL.keys())

def create_population():
    return [random.choice(POOL_KEYS) for _ in range(POP_SIZE)]

def instantiate(name):
    return POOL[name]()

# =========================
# EVOLUTION
# =========================

def evolve(pop, payoffs):

    total = np.sum(payoffs)
    if total == 0:
        return create_population()

    probs = payoffs / total
    new_pop = []

    for _ in range(len(pop)):
        parent = np.random.choice(pop, p=probs)

        if random.random() < MUTATION_RATE:
            parent = random.choice(POOL_KEYS)

        new_pop.append(parent)

    return new_pop

# =========================
# EVOLUTION LOOP
# =========================

def run_evolution(epsilon, seed):

    random.seed(seed)
    np.random.seed(seed)

    pop = create_population()
    history = []

    for gen in range(GENERATIONS):

        pay = np.zeros(len(pop))

        for i in range(len(pop)):

            s1 = instantiate(pop[i])

            for _ in range(MATCHES_PER_AGENT):
                j = random.randrange(len(pop))
                s2 = instantiate(pop[j])

                p1, _ = play_match(s1, s2, epsilon)
                pay[i] += p1

        pop = evolve(pop, pay)

        count = Counter(pop)
        count["Generation"] = gen
        history.append(count)

    return pd.DataFrame(history).fillna(0)

# =========================
# PARALLEL EXECUTION
# =========================

def run_single_seed(args):
    epsilon, seed = args
    df = run_evolution(epsilon, seed)
    df["epsilon"] = epsilon
    return df

def run_experiment():

    results = []

    print(f"Using {MAX_WORKERS} CPU cores")

    for eps in NOISE_LEVELS:

        print("Running epsilon =", eps)

        tasks = [(eps, s) for s in range(SEEDS)]
        seed_runs = []

        with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:

            futures = [executor.submit(run_single_seed, t) for t in tasks]

            for f in as_completed(futures):
                seed_runs.append(f.result())

        results.append(pd.concat(seed_runs))

    return pd.concat(results)

# =========================
# PLOTTING FUNCTIONS
# =========================

def plot_strategy_over_time(df, epsilon):

    sub = df[df["epsilon"] == epsilon]
    avg = sub.groupby("Generation").mean()

    plt.figure()

    for col in POOL_KEYS:
        if col in avg.columns:
            plt.plot(avg.index, avg[col] / POP_SIZE, label=col)

    plt.xlabel("Generation")
    plt.ylabel("Population Share")
    plt.title(f"Strategy Evolution (epsilon={epsilon:.3f})")
    plt.legend()
    plt.savefig(f"evolution_eps_{epsilon:.3f}.png")
    plt.close()

def plot_final_population_vs_noise(df):

    last = df.groupby(["epsilon", "Generation"]).mean().reset_index()
    last = last[last["Generation"] == GENERATIONS - 1]

    plt.figure()

    for strat in POOL_KEYS:
        if strat in last.columns:
            plt.plot(last["epsilon"], last[strat] / POP_SIZE, label=strat)

    plt.xlabel("Noise Level")
    plt.ylabel("Final Population Share")
    plt.title("Population Composition vs Noise")
    plt.legend()
    plt.savefig("phase_diagram.png")
    plt.close()

def plot_naft_survival(df):

    last = df.groupby(["epsilon", "Generation"]).mean().reset_index()
    last = last[last["Generation"] == GENERATIONS - 1]

    plt.figure()
    plt.plot(last["epsilon"], last["NAFT"] / POP_SIZE)

    plt.xlabel("Noise Level")
    plt.ylabel("NAFT Population Share")
    plt.title("NAFT Survival vs Noise")
    plt.savefig("naft_survival.png")
    plt.close()

# =========================
# MAIN
# =========================

if __name__ == "__main__":

    data = run_experiment()
    data.to_csv("evolution_results.csv", index=False)

    plot_final_population_vs_noise(data)
    plot_naft_survival(data)

    for eps in NOISE_LEVELS:
        plot_strategy_over_time(data, eps)

    print("Simulation + plots complete.")
