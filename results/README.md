# Results Data

This directory contains the simulation output data used to produce all figures and tables in the paper.

---

## stationary_results.csv

Output of `src/simulation.py`. Contains empirical stationary distributions and payoffs for TFT and NAFT across 40 noise levels (ε ∈ [0.001, 0.3]).

| Column | Description |
|--------|-------------|
| `epsilon` | Execution noise level ε |
| `piCC_TFT` | Empirical stationary prob. of mutual cooperation under TFT |
| `piCD_TFT` | Empirical prob. of CD state under TFT |
| `piDC_TFT` | Empirical prob. of DC state under TFT |
| `piDD_TFT` | Empirical prob. of mutual defection under TFT |
| `piCC_NAFT` | Empirical stationary prob. of mutual cooperation under NAFT |
| `piCD_NAFT` | Empirical prob. of CD state under NAFT |
| `piDC_NAFT` | Empirical prob. of DC state under NAFT |
| `piDD_NAFT` | Empirical prob. of mutual defection under NAFT |
| `payoff_TFT` | Long-run expected payoff per round for TFT |
| `payoff_NAFT` | Long-run expected payoff per round for NAFT |
| `delta` | Payoff advantage Δ = Π(NAFT) − Π(TFT) |
| `error_TFT` | L2 error between empirical and closed-form stationary dist. (TFT) |
| `error_NAFT` | L2 error between empirical and closed-form stationary dist. (NAFT) |

**Simulation parameters:** 2000 trials × 10,000 rounds, 30 independent seeds, burn-in 200 rounds.  
**Payoffs:** T=5, R=3, P=1, S=0.  
**NAFT parameters:** α=0.6, β=0.2.

---

## evolution_results.csv

Output of `src/evolution.py`. Contains per-generation strategy population counts averaged across 30 seeds, for each of 10 noise levels.

| Column | Description |
|--------|-------------|
| `Generation` | Generation index (0–199) |
| `TFT` | Population count of TFT agents |
| `NAFT` | Population count of NAFT agents |
| `WSLS` | Population count of Win-Stay Lose-Shift agents |
| `Grim` | Population count of Grim Trigger agents |
| `AllC` | Population count of Always Cooperate agents |
| `AllD` | Population count of Always Defect agents |
| `Random` | Population count of Random strategy agents |
| `epsilon` | Execution noise level for this run |

**Simulation parameters:** N=300 agents, 200 generations, 8 matches per agent per generation, µ=0.01 mutation rate, 30 seeds.
