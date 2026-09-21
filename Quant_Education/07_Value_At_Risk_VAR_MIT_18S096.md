# MIT 18.S096: Lecture 7 - Value at Risk (VaR) Models & Enterprise Risk Management

## Comprehensive Educational Notes & Lecture Lexicon

### Core Themes Covered
- Enterprise Risk Architecture: Ken Abbott's Framework at Morgan Stanley (Market, Credit, Operational, Model Risk).
- Value at Risk (VaR) Mathematical Definition: Quantile loss functions and time horizon scaling.
- The Basel Accords: Basel II / III Capital Adequacy Requirements and Supervisory Multipliers.
- Covariance vs Correlation: Co-movement vs Linearity Index (Ken Abbott's Fertilizer & Crop Yield Analogy).
- The Three Canonical VaR Methodologies: Parametric Delta-Normal, Historical Simulation, and Monte Carlo.
- Option Non-Linearity & Greeks: Delta, Gamma Convexity, Vega Volatility Risk, and Greek Hedging.
- Coherent Risk Measures (Artzner et al.): Monotonicity, Translation Invariance, Positive Homogeneity, and Subadditivity.
- The Fatal Flaw of VaR: Violation of Subadditivity in Skewed and Credit Portfolios.
- Expected Shortfall (ES / CVaR): Mathematical Proof of Coherence and Basel III Regulatory Transition.
- Statistical Model Validation: Kupiec POF Likelihood Ratio Test, Christoffersen Independence, and Basel Traffic Lights.
- Enterprise Stress Testing: Historical Scenarios, Reverse Stress Testing, and Liquidity-Adjusted VaR (L-VaR).

### 14-Term Technical Lexicon
1. **Value at Risk (VaR)**: Quantile loss threshold defining maximum expected loss at confidence level 1 - α.
2. **Expected Shortfall (ES)**: Conditional expectation of losses beyond the VaR threshold; coherent risk measure.
3. **Subadditivity Axiom**: Core principle that portfolio combination must never create greater risk than standalone sum.
4. **Delta-Normal VaR**: Analytical closed-form parametric risk calculation under Gaussian asset return assumptions.
5. **Historical Simulation**: Non-parametric empirical quantile evaluation using historical rolling multi-asset returns.
6. **Ghost Features**: False sudden step-function drop in historical VaR when past crisis shocks exit the lookback window.
7. **Kupiec POF Test**: Binomial likelihood ratio hypothesis test evaluating empirical exception frequency against target α.
8. **Christoffersen Test**: Joint likelihood test evaluating both exception frequency and serial independence (clustering).
9. **Basel Traffic Light**: Regulatory zone classification (Green, Yellow, Red) determining capital penalty multipliers.
10. **Stress Testing**: Comprehensive portfolio evaluation under extreme historical crises and hypothetical macro shocks.
11. **Reverse Stress Testing**: Inversion optimization identifying the exact joint asset price shock that causes firm ruin.
12. **Liquidity-Adjusted VaR (L-VaR)**: Augmented risk metric incorporating bid-ask spread unwinding costs.
13. **Gamma Risk (Convexity)**: Second-order option price sensitivity creating accelerating losses during market plummets.
14. **Vega Risk**: Exposure to shifts in market implied volatility driving massive drawdowns on net short option books.
