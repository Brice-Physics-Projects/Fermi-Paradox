# Bayesian Drake Parameters & Distributions

The Bayesian Drake model incorporates uncertainty in each parameter by assigning a probability distribution rather than a fixed value. The chosen distributions reflect current scientific understanding and the degree of uncertainty for each factor.

| Parameter | Distribution Type | Rationale                                                                                                                  |
| --------- | ----------------- | -------------------------------------------------------------------------------------------------------------------------- |
| R*        | Normal            | Measured star formation rate with observational uncertainty with truncation to ensure non-negative values (NASA, Gaia DR3) |
| f_p       | Beta              | Fraction bounded between 0 and 1; informed by Kepler and TESS exoplanet surveys (NASA Exoplanet Archive)                   |
| n_e       | Beta              | Bounded probability with limited empirical constraints (Kepler-derived habitability estimates)                             |
| f_l       | Beta              | No direct observational data; modeled with broad uncertainty (astrobiology literature)                                     |
| f_i       | Beta              | Deep uncertainty regarding emergence of intelligence (no empirical constraints)                                            |
| f_c       | Beta              | Sociotechnical uncertainty in communication behavior (SETI detectability assumptions)                                      |
| L         | Log-normal        | Longevity likely spans orders of magnitude based on historical and theoretical considerations                              |

These distributions are intentionally broad where scientific knowledge is weak. This is a design choice that prioritizes transparency over false precision.

---

## Distribution Types Explained

* **Normal Distribution:** Used for R* due to its empirical measurement with known mean and standard deviation.
* **Beta Distribution:** Ideal for parameters representing fractions (f_p, n_e, f_l, f_i, f_c) since it is bounded between 0 and 1. The shape parameters can be adjusted to reflect different levels of confidence.
* **Log-normal Distribution:** Suitable for L, as civilization longevity can vary over several orders of magnitude, and the log-normal captures this skewed nature.

The Beta distribution is controlled by two shape parameters (α, β) that determine its mean and variance. For example, a Beta(2, 5) distribution has a mean of 0.29 and reflects moderate uncertainty.

* Alpha (α) > Beta (β): Distribution skews toward 1 (higher probabilities)
* Alpha (α) < Beta (β): Distribution skews toward 0 (lower probabilities)
* Alpha (α) = Beta (β): Symmetric distribution centered at 0.5
* Alpha (α) → "successes", Beta (β) → "failures" in a Bernoulli trial context

### Rough Intuition for Beta Distribution

| α     | β  | Shape                      |
| ----- | -- | -------------------------- |
| 1     | 1  | Flat (no prior knowledge)  |
| >1    | >1 | Bell-shaped                |
| α > β | —  | Skewed toward 1            |
| β > α | —  | Skewed toward 0            |
| <1    | <1 | U-shaped (extremes likely) |

---

## Verification of Consistency with Existing Deterministic Drake Logic

The Bayesian Drake model has been cross-checked against the existing deterministic implementation to ensure that when fixed parameter values are used (e.g., means of the distributions), the results align closely. This verification step is crucial to maintain continuity and trust in the model as uncertainty is introduced.

| Parameter | Deterministic Meaning         | Bayesian Meaning      | Match? |
| --------- | ----------------------------- | --------------------- | ------ |
| R*        | Star formation rate           | Star formation rate   | ✅      |
| f_p       | Fraction with planets         | Fraction with planets | ✅      |
| n_e       | Habitable planets per system  | Same                  | ✅      |
| f_l       | Fraction life emerges         | Same                  | ✅      |
| f_i       | Fraction intelligence emerges | Same                  | ✅      |
| f_c       | Fraction communicates         | Same                  | ✅      |
| L         | Communicative lifetime        | Same                  | ✅      |

### Consistency with Deterministic Drake Equation

The Bayesian Drake model preserves full consistency with the classical deterministic Drake Equation.

The underlying equation remains unchanged:

```text
N = R* · f_p · n_e · f_l · f_i · f_c · L
```

* The Bayesian formulation differs only in representation: each parameter is modeled as a probability distribution rather than a fixed scalar value.
* In the limiting case where each distribution collapses to a single value, the Bayesian Drake model reduces exactly to the deterministic Drake calculation.

---

## Default Prior Sets

To encourage transparency and exploration, the Bayesian Drake model supports multiple predefined prior configurations representing different reasonable scientific attitudes toward uncertainty.

| Prior Set    | Description                                                                              |
| ------------ | ---------------------------------------------------------------------------------------- |
| Conservative | Broad distributions biased toward lower probabilities and shorter civilization lifetimes |
| Agnostic     | Maximally uninformative priors reflecting minimal assumptions                            |
| Optimistic   | Distributions biased toward higher probabilities and longer lifetimes                    |

* Users are encouraged to compare outcomes across prior sets to understand how assumptions drive results.
* Specific distribution hyperparameters are defined in the implementation phase and may evolve as new data or assumptions are explored.

---

## Deterministic Drake Equals Bayesian Mean Under Degenerate Priors

When the Bayesian Drake model is configured with degenerate priors (e.g., very tight distributions centered on specific values), the output should converge to the deterministic Drake calculation using those same fixed values. This property ensures that the Bayesian model generalizes the deterministic case.

Conceptually:

* Deterministic Drake (fixed values) ≈ Bayesian Drake (degenerate priors)
* If each Bayesian distribution collapses to a single value
* Then the Monte Carlo samples all produce the same N
* Which equals the deterministic Drake output

### Thought Experiment

1. Set all Bayesian distributions to have near-zero variance around fixed values.
2. Run the Monte Carlo simulation.
3. Observe that all samples yield the same N, matching the deterministic result.

If:

```text
f_p ~ Delta(0.8)
n_e ~ Delta(0.2)
...
```

Then:

```text
Bayesian Drake → deterministic Drake
```

---

## Monte Carlo Sampling Approach

The Bayesian Drake model uses Monte Carlo sampling to propagate uncertainty through the equation:

1. One random value is sampled from each parameter’s distribution
2. The Drake Equation is evaluated using those sampled values
3. The resulting estimate is recorded
4. Steps 1–3 are repeated many times to build a distribution of possible outcomes

Repeating this process thousands (or millions) of times produces a distribution of outcomes representing plausible values for the number of communicative civilizations in the galaxy.

---

## Interpreting the Results

The resulting distribution should **not** be interpreted as a prediction. Instead, it provides insight into:

* plausible ranges of outcomes
* sensitivity to underlying assumptions
* the relative influence of uncertain parameters

In many cases, the median and credible intervals are more informative than the mean, particularly when distributions are skewed or heavy-tailed.

---

## Scientific Rationale

The choice of distributions and prior sets reflects current scientific understanding and acknowledges deep uncertainties in astrobiology. Where empirical data is lacking, broad distributions are used to avoid overconfidence.

---

## Boundaries & Constraints

Each parameter’s distribution is bounded according to physical and logical constraints. For example, fractions are limited to the [0, 1] interval, while longevity spans several orders of magnitude based on theoretical considerations.

This approach ensures that all sampled values remain scientifically plausible.

---

## Limitations & Scientific Honesty

The Bayesian Drake model is a tool for exploring uncertainty, not for making definitive predictions. Its value lies in highlighting how different assumptions impact estimates of communicative civilizations.

Users should approach results with a critical eye, recognizing the limitations of current knowledge and the speculative nature of many parameters.
