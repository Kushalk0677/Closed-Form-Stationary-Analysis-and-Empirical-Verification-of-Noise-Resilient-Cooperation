# Noise-Resilient Cooperation in the Iterated Prisoner's Dilemma

**Approximate Stationary Analysis and Empirical Verification of Noise-Resilient Cooperation in the Iterated Prisoner's Dilemma**

*Submitted to the Journal of Artificial Societies and Social Simulation (JASSS)*

---

## Overview

This repository contains all source code, simulation data, and figures for the paper introducing **NAFT** (Noisy Adaptive Forgiving Tit-for-Tat) — a memory-1 strategy that incorporates controlled stochastic forgiveness to improve cooperative stability in noisy Iterated Prisoner's Dilemma (IPD) environments.

The study demonstrates that:
- Classical Tit-for-Tat (TFT) deteriorates rapidly under execution noise, frequently converging to persistent mutual defection (DD) states
- NAFT maintains substantially higher cooperative mass across low-to-moderate noise regimes
- First-order closed-form stationary approximations closely track NAFT's empirical behavior, while systematically overestimating TFT's cooperation
- NAFT achieves evolutionary dominance at low noise (ε ≤ 0.07), reaching ~48% population share in heterogeneous multi-strategy environments

---

## Repository Structure

```
NAFT-IPD/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── LICENSE                      # MIT License
│
├── src/
│   ├── simulation.py            # Core Markov chain simulation (TFT vs NAFT)
│   ├── evolution.py             # Evolutionary multi-strategy simulation
│   ├── statistical_tests.py     # Statistical significance testing
│   └── ipd_baseline.py          # Baseline IPD evolutionary dynamics
│
├── results/
│   ├── stationary_results.csv   # Stationary distributions & payoffs (40 noise levels)
│   └── evolution_results.csv    # Evolutionary population dynamics (10 noise levels × 30 seeds)
│
├── figures/
│   ├── cooperation_mass.png     # Figure 2: π_CC vs noise level (TFT vs NAFT)
│   ├── mean_payoff_comparison.png  # Figure 1: Payoff performance comparison
│   ├── payoff_dominance.png     # Figure 3: Payoff advantage Δ vs noise
│   ├── stationary_error.png     # Figure 4: Empirical vs closed-form error
│   ├── phase_diagram.png        # Final population share vs noise
│   ├── naft_survival.png        # NAFT survival probability across noise regimes
│   └── evolutionary/
│       ├── epsilon_level_1.png  # Strategy evolution at ε = 0.001
│       ├── epsilon_level_2.png  # Strategy evolution at ε = 0.030
│       ├── epsilon_level_3.png  # Strategy evolution at ε = 0.060
│       ├── epsilon_level_4.png  # Strategy evolution at ε = 0.090
│       ├── epsilon_level_5.png  # Strategy evolution at ε = 0.120
│       ├── epsilon_level_6.png  # Strategy evolution at ε = 0.150
│       ├── epsilon_level_7.png  # Strategy evolution at ε = 0.180
│       ├── epsilon_level_8.png  # Strategy evolution at ε = 0.210
│       ├── epsilon_level_9.png  # Strategy evolution at ε = 0.240
│       └── epsilon_level_10.png # Strategy evolution at ε = 0.300
│
└── paper/
    └── JASSS_Article.pdf        # Full manuscript (anonymised review copy)
```

---

## Strategies

### Tit-for-Tat (TFT)
- Memory-1 vector: **p = (1, 0, 1, 0)**
- Cooperates initially; thereafter mirrors opponent's last action
- Deterministic retaliation makes it highly sensitive to execution errors

### NAFT — Noisy Adaptive Forgiving Tit-for-Tat
- Memory-1 vector: **p = (1, α, 1, β)** with 0 < β < α < 1
- **α** (forgiveness parameter): probability of cooperating after opponent defects — breaks the CD ↔ DC retaliation cycle
- **β** (recovery parameter): probability of cooperating even from mutual defection (DD)
- Default parameters used in paper: α = 0.6, β = 0.2

---

## Key Results

| Noise (ε) | π_CC (TFT) | π_CC (NAFT) | Payoff TFT | Payoff NAFT |
|-----------|------------|-------------|------------|-------------|
| 0.001     | 0.7065     | 0.9964      | 2.416      | 2.997       |
| 0.055     | 0.4573     | 0.8250      | 2.071      | 2.857       |
| 0.100     | 0.4140     | 0.7080      | 2.098      | 2.754       |
| 0.200     | 0.3393     | 0.5168      | 2.157      | 2.574       |
| 0.300     | 0.2915     | 0.3894      | 2.211      | 2.444       |

**Closed-form approximations** (first-order, low-noise):

```
π_CC(TFT)  ≈ 1 / (1 + 2ε)
π_CC(NAFT) ≈ 1 - 2ε / (α + 2ε)

Π(TFT)  ≈ R · [1/(1+2ε)]         + (S+T)/2 · [2ε/(1+2ε)]
Π(NAFT) ≈ R · [1 - 2ε/(α+2ε)]   + (S+T)/2 · [2ε/(α+2ε)]
```

Payoff constants: T = 5, R = 3, P = 1, S = 0

---

## Installation

```bash
git clone https://github.com/Kushalk0677/Closed-Form-Stationary-Analysis-and-Empirical-Verification-of-Noise-Resilient-Cooperation.git
cd Closed-Form-Stationary-Analysis-and-Empirical-Verification-of-Noise-Resilient-Cooperation
pip install -r requirements.txt
```

---

## Running the Simulations

### 1. Core Stationary Analysis (TFT vs NAFT)
Runs the full noise sweep, computes Markov chain stationary distributions analytically and via Monte Carlo, and outputs CSV + figures.

```bash
python src/simulation.py
# Output: results/stationary_results.csv, figures/*.png
# Runtime: ~10–30 min depending on CPU cores (uses multiprocessing)
```

### 2. Evolutionary Multi-Strategy Simulation
Runs 200-generation evolutionary dynamics across 10 noise levels with 30 seeds each.

```bash
python src/evolution.py
# Output: results/evolution_results.csv, figures/phase_diagram.png, figures/naft_survival.png
# Runtime: ~30–60 min
```

### 3. Statistical Significance Test
Runs a paired t-test comparing NAFT vs TFT payoffs at a fixed high-noise level.

```bash
python src/statistical_tests.py
# Output: printed statistics (t-stat, p-value, Cohen's d)
```

### 4. Baseline IPD Evolutionary Dynamics
Early-stage evolutionary simulation with 4-strategy population (no NAFT).

```bash
python src/ipd_baseline.py
# Output: matplotlib plots per epsilon level
```

---

## Reproducibility

All simulations use fixed random seeds for exact reproducibility:
- 30 independent seeds per experiment
- Deterministic under fixed seed selection
- Monte Carlo trials: 2000 per noise level, 10,000 rounds each
- Burn-in: 200 rounds discarded per trial

---

## Citation

If you use this code or results in your work, please cite:

```bibtex
@article{naft_ipd_2025,
  title   = {Approximate Stationary Analysis and Empirical Verification of
             Noise-Resilient Cooperation in the Iterated Prisoner's Dilemma},
  journal = {Journal of Artificial Societies and Social Simulation},
  year    = {2025},
  note    = {Under review}
}
```

---

## License

MIT License — see [LICENSE](LICENSE) for details.
