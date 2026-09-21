# MIT 18.S096: Lecture 5 - Stochastic Processes I: Discrete Time, Markov Chains & Martingales

## Comprehensive Educational Notes & Lecture Lexicon

### Core Themes Covered
- Stochastic Process Foundations: Parameter sets, Trajectories, and Measurability.
- Information Filtrations (ℱ_t): Increasing σ-algebras, Natural filtrations, and Adapted causal processes.
- Discrete-Time Markov Chains (DTMC): First-order Markov property, Transition probability matrices, Chapman-Kolmogorov equations.
- Stationary Distributions (π): Ergodicity, Irreducibility, and Long-run equilibrium states.
- Simple Random Walk: Symmetric vs Asymmetric drift, Reflection Principle, and Path combinatorics.
- Gambler's Ruin Problem: Second-order difference equations, Absorption probabilities, and Infinite-capital house limits.
- Martingale Theory: Rigorous definitions of Martingales, Submartingales, and Supermartingales.
- Stopping Times (Markov Times): Measurability conditions and American option exercise boundaries.
- Doob's Optional Stopping Theorem (OST): 3 Sufficient conditions and proof of the impossibility of fair-game beating systems.
- Doob's Decomposition Theorem: Splitting adapted processes into true Martingale noise and Predictable compensator drift.
- Efficient Market Hypothesis (EMH) and the Mathematical Futility of Doubling Betting Systems.

### 14-Term Technical Lexicon
1. **Filtration (ℱ_t)**: Increasing sequence of σ-algebras modeling information arrival and eliminating lookahead.
2. **Adapted Process**: Property where signal X_t is strictly measurable with respect to historical filtration ℱ_t.
3. **Markov Property**: Memoryless transition dynamic where future distribution depends solely on present state.
4. **Transition Matrix (P)**: Row-stochastic matrix defining multi-state credit and regime migration probabilities.
5. **Chapman-Kolmogorov Equation**: Fundamental composition law P^{(m+n)} = P^m P^n for multi-step Markov paths.
6. **Stationary Distribution**: Invariant left eigenvector π satisfying π^T P = π^T governing long-run regime occupancy.
7. **Simple Random Walk**: Cumulative sum of i.i.d. discrete steps forming the discrete basis for Brownian motion.
8. **Gambler's Ruin Problem**: Analytical absorption framework proving inevitable bankruptcy against infinite-capital counterparties.
9. **Martingale**: Zero-drift fair game where conditional future expectation identically equals the current value.
10. **Submartingale**: Process with non-negative drift (𝔼[X_{n+1}|ℱ_n] ≥ X_n) modeling equity risk premia.
11. **Supermartingale**: Process with non-positive drift (𝔼[X_{n+1}|ℱ_n] ≤ X_n) modeling fee-burdened trading accounts.
12. **Stopping Time (τ)**: Causal random time whose occurrence {τ ≤ n} depends strictly on historical filtration ℱ_n.
13. **Doob's Optional Stopping Theorem**: Establishes conditions under which stopping rules cannot alter expected game outcomes.
14. **Doob's Decomposition**: Unique splitting of financial processes into predictable alpha drift and martingale noise.
