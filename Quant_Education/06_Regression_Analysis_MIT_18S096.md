# MIT 18.S096: Lecture 6 - Regression Analysis: Geometry, OLS & Statistical Foundations

## Comprehensive Educational Notes & Lecture Lexicon

### Core Themes Covered
- The Classical Linear Regression Model: Design Matrix X, Response Y, and Normal Equations.
- The Geometry of Ordinary Least Squares (OLS): Subspace Projection onto Col(X) and Orthogonal Residuals.
- Projection Operators: The Hat Matrix H and Residual Annihilator Matrix M (Idempotence & Symmetry).
- The Gauss-Markov Theorem: Complete Mathematical Proof of Best Linear Unbiased Estimator (BLUE).
- Statistical Inference & ANOVA Decomposition: TSS = ESS + RSS, R^2, Adjusted R^2, t-tests, and F-tests.
- Classical Assumption Violations: Heteroscedasticity, Autocorrelation, Multicollinearity, and Endogeneity.
- Influence & Outlier Diagnostics: Leverage Points h_{ii}, Studentized Residuals, and Cook's Distance.
- Robust Estimation: Huber-White Sandwich Estimator, Newey-West HAC, and Koenker-Bassett Quantile Regression.
- Institutional Applications: Factor Neutralization, Multi-Factor Risk Models, and Tail Risk CAViaR Estimation.

### 14-Term Technical Lexicon
1. **Design Matrix (X)**: Predictor matrix structuring multi-factor risk betas and market explanatory variables.
2. **Ordinary Least Squares (OLS)**: Core parameter estimation minimizing squared Euclidean error distances.
3. **Normal Equations**: Fundamental orthogonality condition (X^T X) β̂ = X^T Y enforcing zero predictor-residual correlation.
4. **Hat Matrix (H)**: Symmetric idempotent projection operator Ŷ = H Y mapping raw responses to fitted subspace values.
5. **Residual Annihilator (M)**: Orthogonal projection operator M = I - H isolating pure idiosyncratic alpha.
6. **Spherical Disturbances**: Homoscedasticity and zero autocorrelation condition required for classical OLS optimality.
7. **Gauss-Markov Theorem**: Mathematical proof guaranteeing minimum variance among all linear unbiased estimators.
8. **Heteroscedasticity**: Non-constant residual error variance across volatility regimes requiring White corrections.
9. **Autocorrelation**: Serial persistence in residual innovations violating independence and inflating test statistics.
10. **Multicollinearity (VIF)**: Linear dependence among predictors inflating estimator covariance and weight instability.
11. **Leverage Point (h_{ii})**: Diagonal element of Hat Matrix quantifying structural pull of individual market observations.
12. **Cook's Distance**: Aggregate parameter displacement metric identifying toxic outlier events in backtest data.
13. **Huber-White Sandwich**: Asymptotically robust covariance matrix correcting for arbitrary heteroscedasticity.
14. **Quantile Regression**: Asymmetric check-loss optimization estimating conditional Value-at-Risk tail quantiles.
