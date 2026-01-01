# Define Default Prior Sets

**Description**
Create predefined prior configurations representing different scientific attitudes toward uncertainty.

_**Tasks**_

* [x] Define hyperparameters for Conservative priors
* [x] Define hyperparameters for Agnostic priors
* [x] Define hyperparameters for Optimistic priors
* [ ] Validate distributions visually
* [ ] Document rationale in scientific theory documentation

_**Notes**

* Ensure that the prior distributions are appropriate for the specific scientific context.
* Consider the impact of prior choices on model inference and interpretation.

## Scope of Prior Application

Priors will initially be applied to key **Drake Equation terms** and **galaxy-scale probability parameters**, including but not limited to:

* \( f_l \) — fraction of habitable planets that develop life  
* \( f_i \) — fraction of life-bearing planets that develop intelligent life  
* Civilization longevity (technological lifetime)  
* Detection probability of interstellar signals

## Prior Selection Guidelines

* **Conservative Priors**: Use when there is strong prior knowledge or when the model should be cautious.
* **Agnostic Priors**: Suitable for situations where little is known, promoting model flexibility.
* **Optimistic Priors**: Employ when there is a strong belief in the model's ability to capture reality.

## Prior Distribution Examples

* **Normal Distribution**: Common for continuous variables with known mean and variance.
* **Uniform Distribution**: Appropriate for variables with no strong prior knowledge.
* **Beta Distribution**: Useful for modeling proportions or probabilities.

## Prior Distribution Implementation

* **Normal Distribution**: Use `scipy.stats.norm` with `loc` and `scale` parameters.
* **Uniform Distribution**: Use `scipy.stats.uniform` with `loc` and `scale` parameters.
* **Beta Distribution**: Use `scipy.stats.beta` with `a` and `b` parameters.

## Implementation Considerations

* **Parameter Selection**: Carefully choose parameters based on domain knowledge and data characteristics.
* **Model Validation**: Validate prior choices through sensitivity analysis and posterior predictive checks.
* **Documentation**: Document prior specifications and their rationale in the model documentation.

## Best Practices

* **Transparency**: Clearly document the choice of priors and their impact on model results.
* **Sensitivity Analysis**: Conduct sensitivity analyses to assess the robustness of model conclusions to prior choices.
* **Model Comparison**: Compare models with different prior specifications to understand the influence of priors on inference.

## Acceptance Criteria

* Three prior sets implemented with explicit numerical parameters
* Each prior visualized with at least one distribution plot
* Prior rationale documented in `docs/05_scientific_theory/`
* Priors selectable programmatically (e.g., via config or UI toggle)

## Conclusion

Prior selection and implementation are critical steps in Bayesian modeling. By following best practices and considering the impact of priors, researchers can ensure robust and interpretable results. Always document prior choices and validate them through appropriate analyses to maintain transparency and reliability in scientific modeling.
