# 🧮 Monte Carlo Simulation Plan for the Drake Equation

## 🌌 Overview

This document outlines the design and implementation strategy for incorporating a **Monte Carlo simulation** into the *Fermi Paradox Simulation Flask App*.  
The Monte Carlo method will be used to estimate uncertainty across all parameters in the **Drake Equation**, producing a probability distribution for the number of detectable civilizations (`N`).  
Later enhancements will extend this approach to model the **probability of inter-civilization detection** by integrating with `prob_detection.py`.

---

## 🎯 Objectives

1. Introduce **probabilistic variability** to the Drake Equation parameters.  
2. Generate **thousands of random scenarios** reflecting the uncertainty in astrophysical estimates.  
3. Produce a **distribution of `N` values** to illustrate the likelihood of different outcomes.  
4. Prepare the framework for a **two-tier simulation**:
   - **Tier 1:** Monte Carlo simulation of the Drake Equation.  
   - **Tier 2:** Feed results into the `prob_detection` model to compute galactic communication probabilities.

---

## 🧠 Conceptual Model

The **Drake Equation**:

\[
N = R^* \times f(p) \times n(e) \times f(l) \times f(i) \times f(c) \times L
\]

Monte Carlo simulation replaces each term with a random value drawn from a **defined probability distribution** (uniform, normal, or triangular), then runs many iterations (e.g., 10,000) to generate a distribution of outcomes.

---

## ⚙️ Implementation Steps

### **Phase 1 – Core Monte Carlo Engine**

1. **Define parameter distributions:**

| Parameter | Description | Suggested Distribution | Range / Mean | Rationale |
|:-----------|:-------------|:------------------------|:--------------|:------------|
| `R*` | Rate of star formation | Uniform | 1 – 3 | Based on Milky Way formation rate |
| `f(p)` | Fraction of stars with planets | Beta (α=3, β=1) | Mean ≈ 0.75 | Skewed toward high likelihood |
| `n(e)` | Number of habitable planets per star | Uniform | 0.1 – 0.3 | Observational uncertainty |
| `f(l)` | Fraction that develop life | Log-uniform | 0.001 – 1 | Highly uncertain biological factor |
| `f(i)` | Fraction that evolve intelligence | Log-uniform | 0.001 – 1 | Anthropocentric uncertainty |
| `f(c)` | Fraction that emit detectable signals | Uniform | 0.05 – 0.3 | Based on technological constraints |
| `L` | Duration of detectable phase (years) | Log-normal | μ = 1e3, σ = 1.5 | Reflects large lifespan uncertainty |

2. **Generate samples:**

```python
samples = 10000
R_star = np.random.uniform(1, 3, samples)
f_p = np.random.beta(3, 1, samples)
n_e = np.random.uniform(0.1, 0.3, samples)
f_l = 10 ** np.random.uniform(-3, 0, samples)
f_i = 10 ** np.random.uniform(-3, 0, samples)
f_c = np.random.uniform(0.05, 0.3, samples)
L = np.random.lognormal(mean=np.log(1e3), sigma=1.5, size=samples)
```

3. **Compute the Drake number:**

```python
N = R_star * f_p * n_e * f_l * f_i * f_c * L
```

4. **Visualize results:**
   - Histogram or kernel density plot (`matplotlib` or `plotly`)
   - Display summary statistics (mean, median, 95% CI)
   - Return data to Flask route as JSON

---

### **Phase 2 – Flask Integration**

1. Create new module:
   ```
   src/fermi_paradox/core/monte_carlo_drake.py
   ```

2. Add Flask endpoint:

```python
@api_bp.route("/simulate-drake", methods=["GET"])
def simulate_drake():
    results = run_monte_carlo(samples=10000)
    mean_N = np.mean(results)
    return jsonify({
        "mean": round(mean_N, 2),
        "median": round(np.median(results), 2),
        "ci_95": [np.percentile(results, 2.5), np.percentile(results, 97.5)],
    })
```

3. Update front-end:
   - Add a “Run Monte Carlo Simulation” button.
   - Use AJAX or Fetch API to trigger the endpoint.
   - Display results as an interactive histogram (e.g., Plotly.js).

---

### **Phase 3 – Integration with Probability Model**

Once the distribution of `N` is established:

1. Pass `N` samples into the polynomial detection model in `prob_detection.py`.  
2. Compute detection probability for each Monte Carlo iteration.  
3. Produce a **2D histogram or heatmap** showing:
   - X-axis: `N` (civilization count)
   - Y-axis: detection probability
   - Color: density or frequency of outcomes

---

## 📊 Example Output

| Statistic | Value |
|:-----------|:------|
| Mean `N` | 8.4 × 10⁶ |
| Median `N` | 3.1 × 10⁶ |
| 95% CI | [4.2 × 10³, 3.2 × 10⁷] |
| Detection Probability (Phase 2) | 0.86 |

---

## 🧩 Next Steps

- [ ] Build `monte_carlo_drake.py` using NumPy & SciPy.  
- [ ] Create Flask API route for simulation.  
- [ ] Integrate Plotly.js visualization on frontend.  
- [ ] Connect Monte Carlo results with detection probability model.  
- [ ] Document results in `/docs/dev_diary/monte_carlo_integration.md`.

---

**“Chance is but the measure of our ignorance.” — Henri Poincaré**
