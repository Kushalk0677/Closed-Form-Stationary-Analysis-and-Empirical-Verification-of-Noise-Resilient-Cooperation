# Closed-Form Stationary Analysis and Empirical Verification of Noise-Resilient Cooperation in the Iterated Prisoner’s Dilemma

The Iterated Prisoner’s Dilemma (IPD) serves as a foundational model for studying
cooperation in repeated strategic interactions. Although Tit-for-Tat (TFT) has historically
been regarded as a robust cooperative strategy, prior work suggests that its performance
degrades under implementation noise due to persistent retaliation cycles and entrapment
in defection states. In this study, we introduce NAFT (Noisy Adaptive Forgiving Tit-for-
Tat), a memory-1 strategy that incorporates controlled stochastic forgiveness to stabilize
cooperation in noisy environments.
We derive closed-form stationary distributions for TFT and NAFT under action noise
using a Markov chain formulation, and prove analytic payoff dominance of NAFT across
the Prisoner’s Dilemma payoff regime. To validate these theoretical predictions, we conduct
large-scale Monte Carlo simulations across a broad noise spectrum, empirically estimating
stationary state occupancies and long-run payoffs. The results demonstrate that NAFT con-
sistently achieves higher cooperative mass, avoids long-term entrapment in mutual defection,
and maintains a statistically significant payoff advantage over TFT in most regimes.
Moreover, the simulations reveal that TFT is substantially more noise-sensitive than pre-
dicted by idealized analytical approximations, as it frequently becomes trapped in persistent
mutual defection states. This finding reframes classical TFT optimality as an upper-bound
phenomenon rather than a practical equilibrium in stochastic environments. Overall, the
study establishes stochastic forgiveness as a mathematically grounded mechanism for sus-
taining long-run cooperation, with implications for evolutionary game theory, multi-agent
systems, and cooperative artificial intelligence
