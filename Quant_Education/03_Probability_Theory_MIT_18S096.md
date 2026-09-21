# MIT 18.S096: Lecture 3 - Probability Theory & Quantitative Statistics

## Comprehensive Educational Notes & Lecture Lexicon

### Core Themes Covered
- Axiomatic Probability Spaces: (Ω, ℱ, ℙ), σ-Algebras, Borel Measurability, and Kolmogorov Axioms.
- Random Variables, Cumulative Distribution Functions (CDF), and Probability Density Functions (PDF).
- Expectation, Variance, Covariance, and Correlation Operators.
- Higher Moments: Skewness (Market Crash Asymmetry) and Excess Kurtosis (Fat Tails / Leptokurtosis).
- Moment Generating Functions (MGF) and Characteristic Functions (Fourier Transform).
- Distribution Taxonomy in Finance: Gaussian, Log-Normal, Student-t (Heavy Tails), and Poisson Jump Models.
- Non-Parametric Tail Bounds: Markov's Inequality, Chebyshev's Inequality, and Cauchy-Schwarz.
- Jensen's Inequality: Mathematical Proof and Fundamental Role in Option Pricing Convexity (Positive Vega).
- Asymptotic Limit Laws: Weak Law (WLLN), Strong Law (SLLN), and Lindeberg-Lévy Central Limit Theorem (CLT).
- Monte Carlo Simulation: O(1 / √N) Error Convergence and Variance Reduction Techniques.

### 14-Term Technical Lexicon
1. **Sigma-Algebra (ℱ)**: Information filtration governing event measurability and martingale adaptations.
2. **Cumulative Distribution Function (CDF)**: Right-continuous monotonic function specifying quantile loss thresholds.
3. **Probability Density Function (PDF)**: Non-negative derivative of CDF enabling analytical risk-neutral expectation pricing.
4. **Moment Generating Function (MGF)**: Transform M_X(t) = 𝔼[e^{tX}] enabling algebraic moment derivation via differentiation.
5. **Characteristic Function**: Fourier transform φ_X(t) = 𝔼[e^{itX}], unconditionally convergent for heavy-tailed returns.
6. **Excess Kurtosis**: Fourth-moment tail thickness metric relative to normal (κ - 3), characterizing market crash risk.
7. **Skewness**: Third standardized moment quantifying distribution asymmetry and option volatility smirk.
8. **Jensen's Inequality**: Invariant g(𝔼[X]) ≤ 𝔼[g(X)] proving why option payoffs benefit from higher market volatility.
9. **Markov's Inequality**: Fundamental distribution-free upper bound on tail exceedance probabilities for non-negative variables.
10. **Chebyshev's Inequality**: Bounded dispersion theorem guaranteeing minimum probability mass within k standard deviations.
11. **Weak Law of Large Numbers (WLLN)**: Convergence in probability of sample averages to theoretical expected returns.
12. **Strong Law of Large Numbers (SLLN)**: Almost-sure pathwise convergence ensuring long-run trading model stability.
13. **Central Limit Theorem (CLT)**: Weak convergence of independent sum innovations to Gaussian distributions.
14. **Monte Carlo Convergence**: Dimension-independent O(1 / √N) precision scaling in derivative simulation pricing.
