# MIT 18.S096: Lecture 2 - Linear Algebra for Quantitative Finance

## Comprehensive Educational Notes & Lecture Lexicon

### Core Themes Covered
- The Four Fundamental Subspaces: Column Space, Nullspace, Row Space, and Left Nullspace.
- The Rank-Nullity Theorem and Orthogonal Complementarity.
- Gram-Schmidt Orthogonalization, Modified Gram-Schmidt, and QR Decomposition.
- Eigenvalues, Eigenvectors, Algebraic vs Geometric Multiplicity, and Defective Matrices.
- The Spectral Theorem for Real Symmetric Matrices (Covariance Matrix Factorization).
- Singular Value Decomposition (SVD): Mathematical Foundations, Singular Values, and Geometric Intuition.
- Eckart-Young-Mirsky Theorem: Truncated SVD, Low-Rank Approximations, and PCA Factor Reduction.
- Matrix Condition Numbers: Inversion Instability in Markowitz Portfolio Optimization.
- Perron-Frobenius Theorem: Non-negative Matrices, Stochastic Transition Matrices, and Markov Stationary Distributions.

### 14-Term Technical Lexicon
1. **Spectral Decomposition**: Orthogonal diagonalization A = Q Λ Q^T for symmetric covariance matrices.
2. **Gram Matrix**: Inner product matrix G = X^T X governing least squares and empirical covariances.
3. **Algebraic Multiplicity**: Multiplicity of an eigenvalue as a root of the characteristic polynomial.
4. **Geometric Multiplicity**: Dimension of the eigenspace Ker(A - λ I); must equal algebraic multiplicity for full diagonalizability.
5. **Defective Matrix**: Lacks a complete eigenbasis (g_i < a_i), requiring Jordan canonical form.
6. **Frobenius Norm**: Matrix Euclidean norm ||A||_F = √(Tr(A^T A)) used in shrinkage calibration.
7. **Condition Number (κ)**: Ratio of maximum to minimum singular values governing inversion stability.
8. **Moore-Penrose Pseudoinverse (A^+)**: Unique generalized inverse for minimum-norm least squares solutions.
9. **Positive Semi-Definite (PSD)**: Property where x^T A x ≥ 0, guaranteeing non-negative portfolio variance.
10. **Singular Value Decomposition (SVD)**: General factorization A = U Σ V^T for rectangular operator systems.
11. **Eckart-Young-Mirsky Theorem**: Proves truncated SVD is the globally optimal low-rank matrix approximation.
12. **Perron-Frobenius Theorem**: Guarantees unique positive dominant eigenvector for irreducible transition matrices.
13. **Stochastic Matrix**: Non-negative row-sum-one matrix defining Markov transition dynamics.
14. **Stationary Distribution (π)**: Long-run steady-state probability vector satisfying π^T P = π^T.
