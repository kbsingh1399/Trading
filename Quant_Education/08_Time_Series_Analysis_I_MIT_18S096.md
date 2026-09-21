# MIT 18.S096: Lecture 8 - Time Series Analysis I: ARMA Models & Forecasting

## Comprehensive Educational Notes & Lecture Lexicon

### Core Themes Covered
- Time Series Foundations: Realization of stochastic processes, Trend, Seasonality, and Noise.
- Strict Stationarity vs Weak (Covariance) Stationarity: Invariance of mean, variance, and lag-autocovariance.
- Autocovariance (γ_k) and Autocorrelation Function (ACF / ρ_k) with Bartlett's Bounds (±1.96 / √N).
- Partial Autocorrelation Function (PACF / φ_{kk}): Direct conditional lag correlation removing intermediate paths.
- Classical Model Taxonomy: White Noise, Autoregressive AR(p), Moving Average MA(q), and ARMA(p, q).
- The Invertibility Condition: Roots of MA polynomial outside the unit circle and AR(∞) causal duality.
- Yule-Walker Equations: Linear matrix solution for closed-form AR parameter estimation.
- Box-Jenkins Signature Diagnostic Matrix: ACF and PACF cutoff rules for model identification.
- Information Criteria for Order Selection: AIC, BIC (Schwarz Bayesian Criterion), and Hannan-Quinn (HQIC).
- Model Diagnostics: Ljung-Box Q-Portmanteau Test for residual white noise verification.
- The Wold Decomposition Theorem: Representation of any covariance-stationary series as infinite moving average shocks.

### 14-Term Technical Lexicon
1. **Covariance Stationarity**: Constant mean, constant finite variance, and lag-only dependent autocovariance.
2. **Strict Stationarity**: Shift-invariance of the complete joint distribution function across all time horizons.
3. **Autocovariance (γ_k)**: Unscaled second-moment covariance between observations separated by lag interval k.
4. **Autocorrelation (ACF)**: Normalized correlation sequence ρ_k = γ_k / γ_0 measuring persistence and decay.
5. **Partial Autocorrelation (PACF)**: Direct lag correlation isolating specific lag impacts by projecting out intermediates.
6. **White Noise (ε_t)**: Uncorrelated zero-mean innovation sequence representing pure market surprise.
7. **Autoregressive Model (AR)**: Dynamic linear regression model where current values depend on own past realizations.
8. **Moving Average Model (MA)**: Finite shock accumulation model where current values depend on past white noise innovations.
9. **Invertibility Condition**: Fundamental root invariant ensuring MA models can be mapped into causal AR(∞) forecasts.
10. **Lag Operator (L)**: Backward-shift linear operator L^k Y_t = Y_{t-k} enabling compact polynomial algebra.
11. **Yule-Walker Equations**: Direct linear system mapping sample autocorrelations into optimal AR parameters.
12. **Akaike Information Criterion (AIC)**: Penalized likelihood criterion balancing fit against complexity to minimize prediction error.
13. **Bayesian Information Criterion (BIC)**: Sample-size scaled penalty criterion providing consistent structural order selection.
14. **Ljung-Box Q-Test**: Portmanteau hypothesis test verifying that model residuals are statistically identical to white noise.
