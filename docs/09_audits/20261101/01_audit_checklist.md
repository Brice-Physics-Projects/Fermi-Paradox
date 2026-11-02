# Audit Checklist 01: Prioritized Action Items

**Source:** [`00_audit_report.md`](00_audit_report.md) (2026-11-01)
**Checked against:** `dev` @ `0b76c0c`

Items are grouped into priority tiers. Within each tier, items are ordered from most to least important.

| Priority | Category |
| --- | --- |
| **P1** | Scientific correctness |
| **P2** | Conflicts and defects within the code |
| **P3** | UI |
| **P4** | Conflicts between docs and code |
| **P5** | Conflicts between docs |

## How to read the item IDs

Each item has two kinds of ID:

- **`P1.1`, `P2.3`, …**: this checklist's own number (priority tier, then position in the tier). Other items use these numbers to refer to each other, e.g. "see P2.10".
- **`[D-1]`, `[C-3, X-9]`, `[§2.3]`, …**: the finding or section in [`00_audit_report.md`](00_audit_report.md) that the item comes from. To see the evidence, file locations, and reasoning behind an item, search the report for that ID.

| Prefix | Meaning | Where in the audit report |
| --- | --- | --- |
| `D-` | Docs vs. code: Drake values and configuration | §2.2, §2.4 |
| `X-` | Conflicts between documentation files | §3 |
| `C-` | Code correctness and security | §4.1 |
| `E-` | Efficiency | §4.2 |
| `S-` | Structure and maintainability | §4.3 |
| `T-` | Tests and CI | §4.4 |
| `§` | A whole report section, for findings without their own ID (e.g. `§2.3` = the "Feature claims vs. reality" table) | as numbered |

Items with no bracketed ID were found while checking the audit against the current code, so they are not in the report.

---

## Already Resolved Since the Audit

- [x] CI now triggers on `main` and `dev` [T-2, §2.4]
- [x] `runtime.txt` removed; Python pinned with `.python-version` [§2.4]
- [x] `pyproject.toml` added and CI migrated to `uv` [S-1] (partially done; see P2.10)

---

## P1: Scientific Correctness

- [ ] **P1.1 Fix the weighted-average `L`** [D-1, C-3]
  - [x] Confirm Drake's 2017 `L` against the cited source (Vaughan, Table 10-1, p. 191). The docs say `1×10⁹`; the code says `1.0E6`.
  - [x] Remove the `/ 2` in `config/drake_number_params.py:9`. The weights 0.2 and 0.8 already sum to 1.
  - [x] Recompute the default N (86,400 now; about 12.96 million if `L_2017 = 1×10⁹`) and update every place it appears.
- [ ] **P1.2 Settle the canonical default values for f_p and f_i** [D-2]
  - [ ] f_p: 0.8 (table, code, UI) or 1.0 (doc justification text)?
  - [ ] f_i: 1 (table, code, UI) or 0.1 (doc justification text)?
- [ ] **P1.3 Add known-answer tests for the Drake equation** [T-1]
  - [ ] Drake 1961 inputs → 7.875×10⁶ (`pytest.approx`)
  - [ ] Drake 2017 inputs → 15.6×10⁶
  - [ ] A test that pins the default N, so a regression like P1.1 fails CI
- [ ] **P1.4 Change n_e's prior from Beta to log-normal or gamma** [X-9]
  - n_e is a count of planets per system, can exceed 1 (Drake 1961 used 3), and the code allows values > 1. A Beta prior breaks the "degenerate priors reduce to deterministic Drake" guarantee.
- [ ] **P1.5 Replace the detection-probability polynomial with the closed form** [C-8]
  - Use `1 − (1 − 1/V)^(n−1) ≈ 1 − e^(−ratio)`. The polynomial is 74 % high at ratio 0.01 and decreases between ratio 4 and 5.
  - Keep `prob_detection.py` only as a validation of the closed form.
- [ ] **P1.6 State the statistical nature of each model** [X-8]
  - [ ] Bayesian Drake = forward Monte Carlo with no likelihood. Remove "posterior predictive checks", "inference", and "properly inferential" wording from its docs.
  - [ ] Fermi hypothesis model = true Bayesian updating over H1–H6. Decide whether PyMC is core or optional.
- [ ] **P1.7 Define the prior sets consistently** [X-6]
  - [ ] Conservative/Optimistic as direction of bias (theory docs), not confidence in the model (`01_02…md`).
  - [ ] Decide whether Uniform is an allowed distribution.
  - [ ] Remove "detection probability of interstellar signals" from the Drake prior scope, or define it as a separate model.
- [ ] **P1.8 Remove claims of validation and endorsement that did not happen**
  - [ ] "The Bayesian Drake model has been cross-checked against the deterministic implementation" (`05_bayesian_drake_parameters.md:42`, `01_01…md:46`): no Bayesian implementation exists. Reword as a requirement.
  - [ ] Uncheck the hyperparameter tasks in `01_02_define_default_prior_sets.md:8-10`; no hyperparameters are defined.
  - [ ] Remove "created with the support of the SETI Institute and the Carl Sagan Center" (`02_drake_number_documentation.md:113`) unless it is true. [D-5]
- [ ] **P1.9 Seed every random generator** [§2.4, E-1]
  - Wire `SIMULATION_SEED` from `.env` into the simulations through `np.random.default_rng(seed)`, as the docs' reproducibility requirement says.
- [ ] **P1.10 Fix the time-dilation figure** [X-15]
  - `04_time_dilation.md:83-85`: a 100,000-year journey at 0.999c (γ = 22.37) takes about **4,470** years of proper time, not 400.
- [ ] **P1.11 Use one value for Earth's radio bubble** [D-4]
  - [ ] Pick one radius: ~100 ly (`01_introduction.md:66`), diameter 200 (`main.py:31`), or `SCALE = 225`, a radius of 112.5 ly (`galaxy_simulator.py:13`).
  - [ ] Replace "about 124 years" with "since ~1901" or compute it.

---

## P2: Conflicts and Defects Within the Code

- [ ] **P2.1 Stop user requests from mutating global defaults** [C-1]
  - `api/routes.py:23` aliases `DEFAULT_DRAKE_PARAMS`. Remove `POST` from `/api/drake`, or use `dict(DEFAULT_DRAKE_PARAMS)`.
- [ ] **P2.2 Stop non-numeric input from returning HTTP 500** [C-2]
  - Resolved by removing `POST` (P2.1), or validate through `DrakeForm`.
- [ ] **P2.3 Accept zero as a valid parameter** [C-5]
  - Change `DataRequired()` to `InputRequired()` in `api/forms/drake_form.py`. Remove the unreachable `if value is None` fallback in `routes.py:58-60`.
- [ ] **P2.4 Fail fast when the production `SECRET_KEY` is missing** [C-6]
  - `config/settings.py:22` silently falls back to `"default_secret_key"`.
- [ ] **P2.5 Make `galaxy_simulator.py` and `prob_detection.py` importable** [C-4, E-4, S-2]
  - [ ] Fix `import prob_detection` (absolute sibling import that also runs the full simulation).
  - [ ] Fix `random.random()` after `from random import random` (AttributeError).
  - [ ] Add the missing `self` to `star_haze`; stop passing values to `spirals` that `__init__` already stores.
  - [ ] Move `tk.Tk()`, `matplotlib.use('TkAgg')`, and `plt.show()` behind `if __name__ == "__main__":`.
  - [ ] Split into pure modules (`core/detection_probability.py`, `core/galaxy_model.py`) and presentation scripts.
  - [ ] Remove the `# noqa: F401` that hides the problems from ruff.
- [ ] **P2.6 Fix the test setup** [T-1]
  - [ ] Pass `TestingConfig` explicitly. Tests now pass only because `DevelopmentConfig` sets `DEBUG=True` and disables the HTTPS redirect.
  - [ ] Set Talisman's `force_https` from config.
  - [ ] Make `test_drake_route_post` assert the recalculated value, and stop it leaking state into other tests.
  - [ ] Add tests for `/api/edit-drake` (valid, invalid, zero values, CSRF) and for non-numeric input.
  - [ ] Use one sanity bound (`< 1e12` vs. `< 1e9`).
- [ ] **P2.7 Fix the double import of the package** [C-10]
  - `run.py` imports `src.fermi_paradox`, which then imports `fermi_paradox.*`. Use `from fermi_paradox import create_app` and drop the `sys.path` hack.
- [ ] **P2.8 Apply `Config.LOG_LEVEL`** [C-12]
  - The config defaults to `INFO`, the logger to `DEBUG`, and the config value is never used.
- [ ] **P2.9 Vectorize or replace the slow Monte Carlo** [E-1]
  - About 122.6 million pure-Python `randint` calls. Use the closed form (P1.5), or NumPy if the Monte Carlo is kept for validation.
- [ ] **P2.10 Finish the `pyproject.toml` migration** [S-1, E-3]
  - [ ] Add a `[build-system]` so the package installs (`uv sync` / `pip install -e .`); then drop `pythonpath = src` from `pytest.ini`.
  - [ ] Move dev-only packages (pytest, ruff, bs4, lxml, stubs) to `[dependency-groups] dev`.
  - [ ] Move Jupyter, matplotlib, pandas, scipy, and sympy to an optional `notebooks` / `science` group.
  - [ ] Remove `nose` (unmaintained, broken on Python ≥ 3.10).
- [ ] **P2.11 Clean up the route layer** [S-3]
  - [ ] Rename the `api` blueprint, which serves HTML, before JSON endpoints arrive (e.g. `pages` at `/drake`, `/drake/edit`).
  - [ ] Replace the hand-written prefill/collect code with `DrakeForm(data=…)` and a dict comprehension.
  - [ ] Remove the unused `name = None` and the unrendered `submit` field.
- [ ] **P2.12 Tighten the Content Security Policy** [C-9]
  - Replace `'unsafe-inline'` with Talisman nonces on the two inline scripts in `base.html`.
- [ ] **P2.13 Configuration hygiene** [S-4, §2.4]
  - [ ] Select the config with `APP_ENV` instead of the deprecated `FLASK_ENV`.
  - [ ] Remove `SQLALCHEMY_TRACK_MODIFICATIONS` (SQLAlchemy is not a dependency).
  - [ ] Put Drake parameter metadata (label, symbol, bounds, default, justification) in one structure and generate the form and tables from it.
- [ ] **P2.14 Code hygiene** [S-5, E-2]
  - [ ] `main.py`: remove the duplicate `__main__` block and the archived-calculation string.
  - [ ] Move the notebook out of `src/fermi_paradox/bayesian_playground/`.
  - [ ] Fix typos: `Calulates`, `calcuate`, `Dectection`, `logrithmic`, `appied`.
  - [ ] Replace `np.pi` with `math.pi` in `galaxy_simulator.py`.
- [ ] **P2.15 CI coverage report** [T-2]
  - Add `--cov-report=xml` (the workflow currently uses only `term-missing`).

---

## P3: UI

- [ ] **P3.1 Fix the `L` formula shown on the Drake page** [D-1]
  - `drake.html:80` and `:95` repeat the `÷ 2` formula. Update it with P1.1.
- [ ] **P3.2 Stop showing default justifications next to user-edited values** [C-7]
  - Show the justification only when the values equal the defaults, or label the column "Default rationale". Do not render a user's `L` as the result of the weighted-average formula.
- [ ] **P3.3 Fix the canonical and Open Graph URLs** [§2.3]
  - `base.html:29` and `:36` point to `devbybrice.com/projects/fermi-paradox`, but the live site is `fermi-paradox-project.com`.
- [ ] **P3.4 Fix `base.html` defects** [C-11]
  - [ ] Remove the second favicon link (`:92`), which returns 404.
  - [ ] Load `style.css` once, after Bootstrap.
  - [ ] Provide `current_year` with a context processor (the footer always shows 2025).
  - [ ] Wrap nav items in `<li>`; no `<div>` directly under `<ul class="navbar-nav">`.
- [ ] **P3.5 Align the home page with what "Probability Detection" will be** [X-7]
  - The home card describes radio-bubble overlap; the roadmap describes FFT signal analysis.
- [ ] **P3.6 Handle placeholder links** [C-11]
  - "Galaxy Simulator" and "Probability Detection" link to `#`. Disable them or point them to a "coming soon" page.
- [ ] **P3.7 Generate `edit-drake.html` fields in a loop** [S-3]
  - It repeats the same 6-line block for 7 fields.

---

## P4: Conflicts Between Docs and Code

- [ ] **P4.1 Fix the README install steps** [§2.3]
  - `README.md:144` runs `pip install -r requirements.txt`, but `requirements.txt` no longer exists. Document `uv sync`, copying `.env.example` to `.env`, and how to start the app.
- [ ] **P4.2 Update the Drake parameter doc to match the code** [D-2]
  - `02_drake_number_documentation.md` gives `L = 1,000` and `L_2017 = 1×10⁹`; apply the values settled in P1.1 and P1.2.
- [ ] **P4.3 Split the architecture docs into "Current" and "Planned"** [§2.1]
  - [ ] `01_project_architecture.md`, `02_structure_description.md`, and the README architecture section.
  - [ ] Correct file names: `drake_number_params.py` (not `drake_params.py`), `galaxy_simulator.py`, `prob_detection.py`, `templates/base.html`.
  - [ ] Document the existing `edit-drake.html` and `bayesian_playground/`.
  - [ ] Mark controllers, schemas, ML, `utils/` helpers, `research/`, and the other templates as planned.
  - [ ] State that the core is pure math and does not validate (or add validation).
  - [ ] Describe `run.py` as the entrypoint; remove the Flask/FastAPI and Pydantic/Marshmallow options.
  - [ ] Fix the README tree path (`src/fermi_paradox/core/`, not `src/core/`).
- [ ] **P4.4 Fix README feature claims and badges** [§2.3, T-2]
  - [ ] Mark Monte Carlo galaxy simulations and the Galaxy Simulation Engine as planned.
  - [ ] Remove "visualize" from the Drake Explorer description, or add a visualization.
  - [ ] Replace the static "Passing" and "Tests: Coming Soon" badges with the live GitHub Actions badge.
  - [ ] Change "Deployment: In Progress" and roadmap Phase 6 to reflect that the site is live.
- [ ] **P4.5 Trim `.env.example`** [D-6, S-4]
  - Only `SECRET_KEY`, `LOG_LEVEL`, and `FLASK_ENV` are read. Remove the other keys or mark them as reserved.
- [ ] **P4.6 Say what happens to the existing galaxy simulator code** [X-11]
  - `09_galaxy_simulator_project_concept.md:4` says implementation has not started, but `core/galaxy_simulator.py` exists. State whether it is reused or replaced.
- [ ] **P4.7 Fix test docstring paths** [S-5]
  - They name `tests/test_api_routes.py` and `tests/test_drake_equation.py`; the files are in subfolders.
- [ ] **P4.8 Update the dependency line in `02_structure_description.md:239`**
  - It still lists `requirements.txt`.

---

## P5: Conflicts Between Docs

- [ ] **P5.1 Make `01_roadmap.md` the single master roadmap** [X-1]
  - [ ] Add the Bayesian Drake, the Fermi hypothesis model, and the time-dilation module.
  - [ ] Rename the phases in the other plans by feature (e.g. "Bayesian Drake: Step 2") and link them from the master.
- [ ] **P5.2 Decide where the Bayesian Drake code lives** [X-4]
  - Separate `core/bayesian_drake.py` (issues, implementation plan) or inside `drake_equation.py` (architecture)?
- [ ] **P5.3 Choose one name for the hypothesis engine** [X-3]
  - `fermi_inference.py`, `fermi_hypothesis.py`, and `evidence_model.py`; add `bayesian_drake.py` to the architecture tree.
- [ ] **P5.4 Choose one path for the Bayesian Drake template** [X-2]
  - `templates/fermi/bayesian_drake.html` or `templates/drake/bayesian_drake.html`; add it to the architecture tree.
- [ ] **P5.5 Reconcile the status of issues 01.01 and 01.02** [X-5]
  - Checked in one file and unchecked in another.
- [ ] **P5.6 Reconcile preset names** [X-6]
  - Optimistic / Conservative / Rare Earth (architecture) vs. Conservative / Agnostic / Optimistic (Bayesian docs).
- [ ] **P5.7 Define what "Probability Detection" means** [X-7]
  - Radio-bubble overlap (home page, code) or SETI-style signal analysis (roadmap, architecture)?
- [ ] **P5.8 Reconcile the galaxy simulator scope** [X-11]
  - Millions of galaxies plus ML surrogate (`07`), static 2D Earth-only reception (`09`), expansion models (`02_galaxy_simulation.md`), or star and planet formation distributions (roadmap).
- [ ] **P5.9 Update `02_structure_description.md` to the new docs layout** [X-12]
  - [ ] Replace the old folder names (`02_scientific_theory`, `03_development_notes`, `04_assets`).
  - [ ] Add the missing folders (`03_datasets`, `04_checklists`, `05_scientific_theory`, `08_api_documentation`, `09_audits`, `10_github_issues`).
  - [ ] Fix the bare `..` and `../../` path artifacts in `01_roadmap.md` and `02_structure_description.md`.
  - [ ] Merge or clearly separate `02_scientific_documentation/` and `05_scientific_theory/`.
- [ ] **P5.10 Deduplicate the Bayesian parameter docs** [X-14, D-3]
  - [ ] Keep the science in `05_scientific_theory/`; make the GitHub-issue files link to it.
  - [ ] Fix the malformed "Rough Intuition" table and the tables missing `| --- |` rows.
  - [ ] Apply the `R*` truncation consistently.
  - [ ] Keep the "Used in Model" column in one place (`01_introduction.md` vs. `02_drake_number_documentation.md`).
- [ ] **P5.11 Choose one dataset location** [X-13]
  - `data/` at the project root or `research/data/`.
- [ ] **P5.12 Align hypothesis wording** [X-10]
  - [ ] H5: avoid detection or avoid contact?
  - [ ] H4: difficult or impossible?
  - [ ] Map "Great Filter ahead" to one of H1–H6 (likely H3).
- [ ] **P5.13 Editorial cleanup** [X-15]
  - [ ] Remove the pasted "Interstellar Travel Module" section from `04_time_dilation.md:162-167`.
  - [ ] Fix the broken list in `03_signal_simulation.md:33-40` and the stacked lead-ins in `02_galaxy_simulation.md:53-54`.
  - [ ] Use the third person in `02_scientific_documentation/*` ("your project").
  - [ ] Fill or renumber the gaps in `05_scientific_theory/` and `00_project_overview/`.
