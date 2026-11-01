# Audit Report 00: Documentation vs. Codebase and Code Quality

**Date:** 2026-11-01
**Branch audited:** `dev` (working tree, including the uncommitted docs restructure)
**Scope:**

1. Documentation vs. codebase: does the code do what the docs describe?
2. Conflicts between documentation files
3. Codebase efficiency, structure, and correctness

**Method:** Every file under `docs/`, `README.md`, all of `src/`, `tests/`, and the root config files (`run.py`, `Procfile`, `runtime.txt`, `pytest.ini`, `.env.example`, `requirements.txt`, `.github/workflows/ci.yml`) were read in full. These checks were run with the project venv (`venv/bin/python`, Python 3.12.3):

| Check | Result |
| --- | --- |
| `pytest` | 8 passed |
| `ruff check src/fermi_paradox` | All checks passed |
| Default Drake number (`DEFAULT_DRAKE_PARAMS`) | `L = 5,400,000`, `N = 86,400` |
| Runtime behavior probes (Flask test client) | See findings C-1, C-2, C-3, C-11 |
| `import galaxy_simulator` | Hangs (killed after 5 s); see C-4 |

Severity key: 🔴 High (wrong results, crashes, or security), 🟠 Medium (misleading docs, broken features, maintainability), 🟢 Low (cleanup and polish).

---

## 1. Executive Summary

- **The only working feature is the deterministic Drake calculator** (`core/drake_equation.py` with the `/api/drake` and `/api/edit-drake` routes). The docs describe a much larger system (controllers, ML layer, Bayesian engines, visualization, research workspace), and most of it does not exist yet. Several docs describe planned modules **as if they already exist**.
- **There are three significant correctness bugs in the live Drake feature:**
  1. User POSTs to `/api/drake` permanently overwrite the global default parameters for every later visitor.
  2. A non-numeric input causes an HTTP 500.
  3. Valid zero inputs are rejected by the edit form.
- **The scientific value of `L` is wrong in two ways:**
  1. The "weighted average" formula divides by 2 even though its weights already sum to 1.
  2. The 2017 value of `L` in the code (`1.0E6`) contradicts the docs (`1×10⁹`).
- **`core/galaxy_simulator.py` and `core/prob_detection.py` are standalone scripts, not modules.** Importing them opens a Tk window, runs about 122 million random draws, and blocks on `plt.show()`. `galaxy_simulator.py` also has runtime bugs that would crash it.
- **The docs contain at least four competing roadmaps** with conflicting phase numbering, three different file names for the hypothesis engine, two different paths for the Bayesian Drake template, and conflicting completion status for the same GitHub issue.

---

## 2. Documentation vs. Codebase

### 2.1 Documented structure vs. actual structure

Sources: `docs/01_architecture/01_project_architecture.md` (tree), `docs/01_architecture/02_structure_description.md`, and `README.md` (Architecture Overview).

| Documented | Actual | Status |
| --- | --- | --- |
| `config/drake_params.py` with named presets (Optimistic, Conservative, Rare Earth) | `config/drake_number_params.py` with a single `DEFAULT_DRAKE_PARAMS` dict and no presets | ❌ Name differs; presets missing |
| `core/drake_equation.py`: "deterministic **and Bayesian** Drake models" (architecture) and "pure math **and validation**" (structure) | Only a deterministic one-line product with no validation | ❌ |
| `core/galaxy_simulation.py`: "Monte Carlo simulation… uses Drake results as probabilistic inputs" | `core/galaxy_simulator.py`: a Tkinter drawing script; `NUM_CIV = 15_600_000` is hard-coded rather than taken from the Drake module | ❌ Name and behavior differ |
| `core/probability_models.py`: signal natural-vs-artificial statistics, FFT | `core/prob_detection.py`: a radio-bubble overlap Monte Carlo with a polynomial fit (no FFT or signal work) | ❌ Name and purpose differ |
| `core/fermi_inference.py`, `core/visualization.py` | Do not exist | ❌ Planned, but described in the present tense |
| `ml/surrogate/`, `ml/signal_detection/` | Do not exist (the structure doc says "scaffolded… intentionally empty", but there is no scaffold) | ❌ |
| `api/controllers/*.py`, `api/routes/routes.py`, `api/schemas.py`; "Routes should be thin and delegate to controllers" | `api/routes.py` only; business logic lives in the routes; no controllers or schemas | ❌ |
| `api/forms/galaxy_simulation_form.py`, `signal_detection_form.py` | Only `drake_form.py` | ❌ |
| `templates/base/base.html`, `templates/base/home.html` | `templates/base.html`, `templates/home.html` (no `base/` folder) | ❌ |
| `templates/fermi/`, `templates/galaxy_simulator/`, `templates/signal_detection/` | Do not exist | ❌ |
| `templates/drake/edit-drake.html` | Exists but is **not documented** anywhere | ⚠️ |
| `utils/math_helpers.py`, `formatters.py`, `plot_utils.py` | `utils/` contains only `__init__.py` | ❌ |
| `research/notebooks/`, `research/references/`, `research/data/` | No `research/` directory. The only notebook is in `src/fermi_paradox/bayesian_playground/`, inside the deployable package. | ❌ |
| `bayesian_playground/` package | Exists but is **not documented** in any architecture doc | ⚠️ |
| `pyproject.toml` (architecture tree and structure §13) | Does not exist | ❌ |
| `main.py`: "Application entrypoint… responsible ONLY for initializing the Flask app" | The production entrypoint is `run.py` (via `Procfile`). The app factory is in `__init__.py`. `main.py` also contains a duplicated `if __name__ == "__main__"` block and a commented-out "archived calculations" string. | ⚠️ |
| "Flask/FastAPI" (architecture, structure §2.1 and §6) and "Pydantic or Marshmallow" (structure §6) | Flask only; no schema library | ⚠️ Stale optionality |
| README tree: `src/core/`, `src/api/`, … | Actual path is `src/fermi_paradox/core/`, … | ❌ Missing a level |
| Core layer: "No web framework code… These modules should be importable independently" | `galaxy_simulator.py` creates a `tk.Tk()` window at import time, and `prob_detection.py` runs a full simulation plus `plt.show()` at import time | ❌ Violates the stated architecture |

**Recommendation:** Split each architecture doc into two clearly labeled sections, **"Current (as built)"** and **"Target (planned)"**, or mark planned items inline (e.g. `(planned)`). Right now a reader cannot tell what exists.

### 2.2 Drake parameter values: docs vs. code vs. UI

| Parameter | `02_drake_number_documentation.md` table ("Used in Model") | Same doc, justification text | `drake_number_params.py` (code) | `drake.html` (UI text) |
| --- | --- | --- | --- | --- |
| R* | 2 | 2 | 2 | 2 |
| f_p | **0.8** | **1.0** ("A value of 1.0 is used") | 0.8 | 0.8 |
| n_e | 0.2 | 0.2 | 0.2 | 0.2 |
| f_l | 0.5 | 0.5 | 0.5 | 0.5 |
| f_i | **1** | **0.1** ("This model uses f(i) = 0.1") | 1 | 1.0 |
| f_c | 0.1 | 0.1 | 0.1 | 0.1 |
| L | **1,000** | **1,000** | **5,400,000** (weighted average) | Weighted average, shown as 5,400,000 |
| Drake 2017 `L` | **1×10⁹** | — | `L_2017 = 1.0E6` | "2017 (1.0×10⁶ years)" |

🔴 **D-1: `L` is computed incorrectly.** Code: `drake_number_params.py:9`. The UI repeats the formula at `drake.html:80` and `drake.html:95`.

- The code computes `L = (0.2·L_1961 + 0.8·L_2017) / 2`. The weights 0.2 and 0.8 already sum to 1, so dividing by 2 halves the weighted mean. With the code's own inputs, the correct weighted mean is **10,800,000**, not 5,400,000.
- `L_2017` is `1.0E6`, but both `01_introduction.md:58` and `02_drake_number_documentation.md:38` give Drake's 2017 value as **1×10⁹**. That value is the one consistent with the documented 2017 result: N = 3 × 1 × 0.2 × 0.13 × 1 × 0.2 × 1×10⁹ = **15.6×10⁶**. It is also what `galaxy_simulator.py:15` hard-codes (`NUM_CIV = 15_600_000`).
- If `L_2017 = 1×10⁹` is correct, the 80/20 weighted mean becomes `0.2·50e6 + 0.8·1e9 = 810,000,000`. That changes the displayed N from 86,400 to about 12.96 million.
- **Action:** Confirm `L_2017` against the cited source (Vaughan, Table 10-1, p. 191). Remove the `/ 2`. Then update the code, the UI text, and `02_drake_number_documentation.md` together.

🟠 **D-2: `02_drake_number_documentation.md` contradicts itself** on f_p (table 0.8, text 1.0), f_i (table 1, text 0.1), and L (1,000 in the doc, about 5.4M in the code). The UI's justification text (`drake.html:48`, `drake.html:66`) agrees with the code, not with the doc text.

🟢 **D-3:** `01_introduction.md:50-59` has a "Used in Model" column filled with "—" while `02_drake_number_documentation.md` has values. The same table is maintained in two places.

🟢 **D-4:** Earth's radio bubble is given three ways:

- `01_introduction.md:66`: radius ~100 ly
- `main.py:31`: diameter 200
- `galaxy_simulator.py:13`: `SCALE = 225`, "Enter 225 to see Earth's radio bubble", i.e. a radius of 112.5 ly

`02_drake_number_documentation.md:96` says Earth has transmitted for "about 124 years (since around 1901)". That was correct in 2025; it is 125 years as of this audit. Compute it or phrase it as "since ~1901".

🟠 **D-5: Unverified claim.** `02_drake_number_documentation.md:113` says the doc "was created with the support of the SETI Institute and the Carl Sagan Center". Remove it unless that support actually happened, because it implies an endorsement.

### 2.3 Feature claims vs. reality

| Claim | Location | Reality |
| --- | --- | --- |
| "Run **Monte Carlo galaxy simulations**" (users can) | `README.md:60` | No route or UI. The nav shows "Galaxy Simulator (Coming Soon)". |
| "Galaxy Simulation Engine: Monte Carlo simulations that model civilization emergence, spatial/temporal overlap, galactic habitability" (no "planned" tag) | `README.md:76-82` | Not implemented |
| "Drake Equation Explorer… **visualize** how they impact estimates" | `README.md:71-74` | There is a number and a table but no visualization |
| Tests badge "Coming Soon" | `README.md:20` | 8 tests exist and CI runs pytest with coverage |
| Build badge "Passing" | `README.md:19` | A static shields.io badge, not linked to CI status |
| "Deployment: In Progress"; roadmap Phase 6 "Optional deployment (Heroku, AWS…)" | `README.md:22`, `01_roadmap.md:157` | The app is already live (`README.md:5`) with a Heroku `Procfile` |
| Install: `pip install -r requirements.txt && flask run` | `README.md:141-146` | `flask run` only finds the app if `FLASK_APP` is set. That happens only after copying `.env.example` to `.env`, a step the README does not mention. |
| Live URL `https://fermi-paradox-project.com` | `README.md:5` | `base.html:29` and `base.html:36` set canonical and OG URLs to `https://www.devbybrice.com/projects/fermi-paradox`, which tells search engines a different site is the original |
| Roadmap Phase 1 deliverable "Testing scaffolding" | `01_roadmap.md:30` | Done, but the README badge says otherwise |
| `05_bayesian_drake_parameters.md:42`: "The Bayesian Drake model **has been cross-checked** against the existing deterministic implementation" | `docs/05_scientific_theory/` (repeated in `10_github_issues/…/01_01…md:46`) | **No Bayesian implementation exists**, so this cross-check cannot have been done. Reword it as a design requirement ("must reduce to…"). |
| `01_02_define_default_prior_sets.md:8-10`: hyperparameter tasks checked `[x]` | `docs/10_github_issues/…` | No hyperparameters are defined anywhere in docs or code. `05_bayesian_drake_parameters.md:76` says they are "defined in the implementation phase". |
| Home page "Probability Detection Model… Monte Carlo simulations and polynomial regression" | `home.html:54-63` | Matches `prob_detection.py`, but **not** the architecture or roadmap meaning of "Probability Detection" (FFT/SETI signal analysis). See conflict X-7. |

### 2.4 Configuration and deployment docs vs. code

- 🟠 **D-6: Most of `.env.example` is unused.** These variables are read by no code: `APP_ENV`, `API_TITLE`, `API_VERSION`, `GALAXY_SIM_DEFAULT_RUNS`, `SIMULATION_SEED`, `SURROGATE_MODEL_PATH`, `SIGNAL_CLASSIFIER_PATH`, `ENABLE_RATE_LIMITING`, `RATE_LIMIT_*`, `NASA_API_KEY`, `OPENAI_API_KEY`, `WOLFRAM_ALPHA_APPID`, `DATABASE_URL`, `HOST`, and `WORKERS`. Only `SECRET_KEY`, `LOG_LEVEL`, and `FLASK_ENV` are read. `SIMULATION_SEED` matters most, because the docs require reproducible seeds and the simulations never seed their random generators.
- 🟢 `settings.py:25` sets `SQLALCHEMY_TRACK_MODIFICATIONS`, but SQLAlchemy is not a dependency.
- 🟢 **CI triggers on the wrong branches.** `ci.yml` runs on `main` and `src/refactor`. Active work is on `dev`, so pushes to `dev` are never tested.
- 🟢 `runtime.txt` is the legacy way to pin Heroku's Python version. Heroku now prefers `.python-version`; check their current docs before the next deploy.

---

## 3. Conflicts Between Documentation Files

Each row lists the files involved and what conflicts.

### X-1 🟠 Four competing roadmaps with clashing phase numbers

| File | Phase 1 | Phase 2 | Phase 3 | Later |
| --- | --- | --- | --- | --- |
| `docs/04_checklists/01_roadmap.md` | Foundation | **Galaxy Simulation Engine** | Probability & **Signal** Detection (FFT) | 4 Visualization, 5 ML, 6 Publication |
| `docs/00_project_overview/06_bayesian_drake__implementation.md` | Scientific model finalization (Bayesian) | **Core Bayesian Engines** | API & Controllers | 4 UI, 5 Viz, 6 Docs, 7 Release |
| `docs/00_project_overview/09_galaxy_simulator_project_concept.md` §10 | Synthetic population | **Earth-directed reception** | Repeated experiments | 4 Website viz, 5 Extensions |
| `README.md` versioning and roadmap | v0.x Exploration | v1.x Simulation | v2.x ML | v3.x Publication |

- The master roadmap (`01_roadmap.md`) **does not mention the Bayesian Drake or Fermi-hypothesis work at all**. That is the work the GitHub-issues folder is actively tracking, and the architecture's core pipeline ("Drake → Civilization Simulation → Observational Constraints → Bayesian Hypothesis Inference", `01_project_architecture.md:9`) depends on it.
- The roadmap also omits the time-dilation / "Relativistic Travel Engine" module described in `02_scientific_documentation/04_time_dilation.md`.
- "Phase 2" means three different things depending on which file you read.
- **Action:** Make `01_roadmap.md` the single master roadmap. Treat the other plans as feature-level sub-plans named by feature (e.g. "Bayesian Drake: Step 2"), and link them from the master.

### X-2 🟠 Bayesian Drake template path

- `06_bayesian_drake__implementation.md:164` → `templates/fermi/bayesian_drake.html`
- `10_github_issues/00_github issues.md:269` → `templates/drake/bayesian_drake.html`
- `01_project_architecture.md:157-175` lists neither; it has only `fermi/hypothesis_model.html`.

### X-3 🟠 Hypothesis / inference engine module name

- `01_project_architecture.md:74` → `core/fermi_inference.py`
- `06_bayesian_drake__implementation.md:97` → `core/fermi_hypothesis.py`, plus a separate `core/evidence_model.py` (`:114`) that the architecture doesn't list
- `06_bayesian_drake__implementation.md:80` and `00_github issues.md:196` → `core/bayesian_drake.py`, which the architecture tree doesn't list

### X-4 🟠 Where the Bayesian Drake code lives

- `01_project_architecture.md:63-65`: `drake_equation.py` "implements deterministic **and Bayesian** Drake models"
- `00_github issues.md:128` and `:242`, and `06_bayesian_drake__implementation.md:80` and `:139`: Bayesian Drake goes in a separate `core/bayesian_drake.py`, and the deterministic Drake logic stays **untouched**

### X-5 🟠 Issue 01.01 and 01.02 status

- `00_github issues.md:148-154`: issue 01.01 tasks all `[x]`
- `06_bayesian_drake__implementation.md:17-33`: the same work ("Define Drake parameters", "Select distributions", "Document rationale") is all `[ ]`
- `00_github issues.md:165-169`: 01.02 hyperparameter tasks are `[ ]`
- `10_github_issues/…/01_02_define_default_prior_sets.md:8-10`: the same tasks are `[x]`

### X-6 🟠 Meaning of the prior sets

- `05_scientific_theory/02_bayesian_drake_model.md:67-71` and `05_bayesian_drake_parameters.md:69-73`:
  - **Conservative** = "biased toward lower probabilities and shorter lifetimes"
  - **Optimistic** = "biased toward higher probabilities and longer lifetimes"
- `10_github_issues/…/01_02_define_default_prior_sets.md:30-32`:
  - **Conservative** = "use when there is strong prior knowledge or when the model should be cautious"
  - **Optimistic** = "when there is a strong belief in the model's ability to capture reality"
- These are different concepts. The first describes the **direction of bias** in a parameter. The second describes **confidence** in the model.

Related conflicts:

- `01_project_architecture.md:49-52` and `02_structure_description.md:46` name the config presets **Optimistic / Conservative / Rare Earth**. The Bayesian docs name the prior sets **Conservative / Agnostic / Optimistic**.
- `01_02…md:37` and `:43` add a **Uniform** distribution. Both theory docs allow only Normal, Beta, and Log-normal.
- `01_02…md:21-26` applies priors to "**detection probability of interstellar signals**", which is outside the Drake parameters that every other Bayesian doc covers.

### X-7 🟠 What "Probability Detection" means

- `home.html:54-63` and the code (`prob_detection.py`): probability that radio **bubbles overlap in space** (Monte Carlo plus polynomial regression)
- `01_roadmap.md:63-83`, `01_project_architecture.md:90-94`, and `02_structure_description.md:66-69`: SETI-style **signal analysis** (FFT, noise modeling, natural-vs-artificial scoring)
- The nav item "Probability Detection (Coming Soon)" will therefore deliver something different from what the home page promises.

### X-8 🟠 Bayesian inference vs. forward Monte Carlo

- `05_scientific_theory/02_bayesian_drake_model.md:27-33`: the model "does **not** attempt to infer parameter values… **rather than** full Bayesian inference with likelihood updating"
- `01_02_define_default_prior_sets.md:49` calls for "**posterior predictive checks**", and `:55` and `:67` refer to "inference". Posterior checks require a likelihood or posterior.
- `00_github issues.md:51` calls the Bayesian Drake "Properly inferential". The theory doc says it is forward modeling.
- `08_bayesian_model_fermi.md:100-126` recommends PyMC with `pm.sample` (true posterior inference) as the implementation. `06_bayesian_drake__implementation.md:244` and `00_github issues.md:382` list PyMC as an "optional future" enhancement.
- **Action:** State explicitly that there are two models. (a) The Bayesian Drake is forward Monte Carlo and has no likelihood. (b) The Fermi hypothesis model uses real Bayes updates over H1–H6. Then align the wording.

### X-9 🟠 n_e modeled as a Beta distribution (bounded in [0, 1])

- `05_bayesian_drake_parameters.md:9` and `:20`, `02_bayesian_drake_model.md:53`, and `01_01…md:9` assign n_e a **Beta** distribution and call it a "fraction".
- `02_drake_number_documentation.md:9` and `:34`, `01_introduction.md:37`, and `02_scientific_documentation/01_drakes_number.md:23` define n_e as the "average **number** of planets per system", which can exceed 1. Drake's own 1961 value was **n_e = 3** (`02_drake_number_documentation.md:34`). The code also allows n_e > 1 (`drake_form.py:16` sets only `min=0`).
- A Beta prior cannot reproduce Drake's 1961 inputs. That breaks the docs' own "degenerate priors reduce to deterministic Drake" guarantee (`05_bayesian_drake_parameters.md:78-100`). **Action:** Use a log-normal or gamma distribution for n_e.

### X-10 🟢 Hypothesis wording

- H5: "avoid **detection**" (`01_project_architecture.md:87`), "intentionally avoid **contact**" (`06…md:47`), "deliberately avoid contact" (`08…md:25`)
- H4: "Interstellar expansion is difficult" (architecture) vs. "travel or expansion is **impossible** or extremely difficult" (`08`)
- `06…md:121` maps high civilization counts to "**Great Filter ahead**", which is not one of H1–H6. The closest is H3. `08…md:177` also uses the Great Filter framing.

### X-11 🟠 Galaxy simulator scope

- `00_project_overview/07_galaxy_mc_simulator.md`: simulate "**millions of possible galaxies**" from Drake-parameter distributions, then train an **ML surrogate** (Random Forest/XGBoost/MLP). Outputs include "contact probability".
- `00_project_overview/09_galaxy_simulator_project_concept.md:26` and `:30`: recommended first scope is a **static 2D synthetic galaxy with Earth-only reception**. It explicitly excludes expansion (`:47`) and warns that sampled results must not be read as galaxy-wide claims (`:142`).
- `02_scientific_documentation/02_galaxy_simulation.md` §3 centers on **civilizational expansion models** (diffusion, frontier, cluster, reversible), which `09` excludes from the first milestone.
- `01_roadmap.md:44-50` Phase 2 instead focuses on probability distributions for star formation and planet formation, with heatmap and scatter visualizations.
- `09…md:4` says "implementation has not been verified or started", but a Tkinter galaxy renderer already exists in `core/galaxy_simulator.py`. The concept doc does not say whether that code is to be reused or replaced.

### X-12 🟠 Docs folder layout after the restructure

- `01_architecture/01_project_architecture.md:204-214` lists the current folders: `02_scientific_documentation`, `06_development_notes`, `07_assets`, and so on.
- `01_architecture/02_structure_description.md:202-226` still lists the **old** layout:
  - `02_scientific_theory/`, which is now `02_scientific_documentation/` (and a separate `05_scientific_theory/` exists)
  - `03_development_notes/`, which is now `06_development_notes/` (`03` is now `03_datasets`)
  - `04_assets/`, which is now `07_assets/` (`04` is now `04_checklists`)
  - It also says `00_project_overview/` contains the roadmap, which now lives in `04_checklists/`.
  - It omits `03_datasets`, `04_checklists`, `05_scientific_theory`, `08_api_documentation`, `09_audits`, and `10_github_issues`.
- The relative paths were left broken by the file moves:
  - `01_roadmap.md:22` and `:154` contain a bare `` `..` `` where a docs path used to be.
  - `02_structure_description.md:13-15`, `:21`, `:23`, `:160`, `:198`, and `:236-241` use `` `../../src` ``, `` `..` ``, `` `../../tests` ``, and `` `../../.env` ``. These look like they came from a find-and-replace of relative links.
- Having two science folders (`02_scientific_documentation/` and `05_scientific_theory/`) with overlapping purposes is itself confusing.

### X-13 🟢 Dataset location

- `03_datasets/01_datasets.md:217` → `data/raw/`, `data/processed/`, `data/simulated/` at the project root
- `01_project_architecture.md:196` and `02_structure_description.md:189` → `research/data/`

### X-14 🟢 Duplicated content that will drift

- `05_scientific_theory/05_bayesian_drake_parameters.md` and `10_github_issues/…/01_01_define_bayesian_drake_parameters.md` are near-identical copies. They have already diverged: the theory doc has a malformed "Rough Intuition" table (lines 32-38, columns shifted), while the issue copy fixed that table but dropped the header-separator rows (`| --- |`) in three other tables (lines 5-6, 48-49, 77-78), so those tables **will not render** as tables.
- `05_scientific_theory/02_bayesian_drake_model.md` and `05_bayesian_drake_parameters.md` repeat the same "Default Prior Sets", "Monte Carlo Sampling Approach", and "Interpreting the Results" sections. `R*` truncation appears in one but not the other (`02…md:51` vs. `05…md:7`).
- **Action:** Keep the science in `05_scientific_theory/` only. GitHub-issue files should link to it rather than copy it.

### X-15 🟢 Scientific and editorial errors inside individual docs

- `02_scientific_documentation/04_time_dilation.md:83-85`: "A 100,000-year journey… might feel like **400 years** to the travelers at 0.999c." With γ = 22.37 (the doc's own table, line 79), proper time is 100,000 / 22.37 ≈ **4,470 years**. The γ values in the table are correct.
- `04_time_dilation.md:162-167`: a trailing "🚀 Interstellar Travel Module" section looks pasted from the README and is out of place.
- `03_signal_simulation.md:33-40`: §1.3 "Civilizations may:" is followed by an unrelated list (Diplomacy, Coordination…), so the sentence is broken.
- `02_galaxy_simulation.md:53-54`: two stacked lead-in sentences ("based on:" followed by "Each star system can have…").
- The `02_scientific_documentation/*` files address the reader as "your project", while the rest of the docs use the third person.
- `05_scientific_theory/` numbering has gaps (`02`, `05`; no `01`, `03`, or `04`). `00_project_overview/` skips `04` and `05` after the moves.

---

## 4. Codebase Correctness, Efficiency, and Structure

### 4.1 Correctness and security (ordered by severity)

🔴 **C-1: Shared global state is modified by user requests.** `api/routes.py:22-27`

```python
params = DEFAULT_DRAKE_PARAMS          # alias, not a copy
...
params[key] = float(value)             # mutates the module-level dict
```

**Verified:** after one `POST /api/drake` with `L=1`, `DEFAULT_DRAKE_PARAMS['L']` stayed at `1.0` for the rest of the process. Every later visitor (and the edit form's prefill) sees the altered defaults until the worker restarts, and different gunicorn workers will show different values. It also couples the tests: `test_drake_route_post` changes `L` for every test that runs after it. **Fix:** `params = dict(DEFAULT_DRAKE_PARAMS)`. Since no UI form POSTs to `/api/drake`, the simpler fix is to drop `POST` from this route.

🔴 **C-2: Unvalidated input crashes the request.** `api/routes.py:25-27`
**Verified:** `POST /api/drake` with `L=abc` raises `ValueError` (HTTP 500 in production). The route also accepts negative values and fractions above 1 for f_* parameters. **Fix:** Remove POST, or validate it through `DrakeForm`.

🔴 **C-3: Scientific error in `L`.** See D-1. The "weighted mean" is off by a factor of 2, and possibly by a factor of 150 if the 2017 `L` value is wrong.

🔴 **C-4: `core/galaxy_simulator.py` cannot run as written.**

- `:5` `import prob_detection` is an absolute import of a sibling file. It fails with `ModuleNotFoundError` when imported as `fermi_paradox.core.galaxy_simulator`. When it does resolve, it **runs the whole Monte Carlo and blocks on `plt.show()`** (verified: the import hung).
- `:24-28` create a `tk.Tk()` window at import time. This fails on headless hosts (Heroku, CI).
- `:127` calls `random.random()`, but `random` was imported as a *function* (`from random import random`), so this raises `AttributeError`.
- `:176` `def star_haze(disc_radius_scaled, random_polar_coordinates, density)` is an instance method missing `self`. It also takes a function argument instead of using `self.random_polar_coordinates`.
- `:136` `spirals(self, b, r, rot_fac, fuz_fac, arm)` takes the same values that `__init__` stores on `self`, so the attributes are duplicated and unused.
- `ruff` passes only because of `# noqa: F401`, and coverage never reaches these files because no test imports them.

🟠 **C-5: The edit form rejects valid zero values.** `api/forms/drake_form.py:14-20`
`DataRequired()` treats `0.0` as missing. **Verified:** submitting `f_c=0` re-renders the form with a "required" error. Zero is a scientifically meaningful input ("life never arises"). **Fix:** use `InputRequired()`. The `if value is None` fallback in `routes.py:58-60` is unreachable under either validator.

🟠 **C-6: Weak production secret key.** `config/settings.py:22`
`SECRET_KEY` silently falls back to `"default_secret_key"`. If the env var is ever missing in production, CSRF tokens and session cookies are signed with a public key. **Fix:** have `ProductionConfig` raise at startup when `SECRET_KEY` is unset.

🟠 **C-7: Wrong justification text after user edits.** `templates/drake/drake.html:42-80`
The "Justification" column is hard-coded to the defaults ("Model uses 0.2", "Value 0.8 chosen…"). After a user edits the parameters, the page shows the user's values next to text justifying different values. It also renders `L = (0.2×50E6 + 0.8×1.0E6) ÷ 2 = {user's L}`, which presents an arbitrary user value as the result of that formula. **Fix:** show the justification only when the values equal the defaults, or label the column "Default rationale".

🟠 **C-8: The detection-probability polynomial is inaccurate and non-monotonic.** `galaxy_simulator.py:100-106` and `prob_detection.py`
The 4th-order fit approximates a quantity with a closed form. For V equal-sized volumes and n civilizations, the probability that a given civilization shares its volume is `1 − (1 − 1/V)^(n−1) ≈ 1 − e^(−ratio)`. Comparison:

| ratio | polynomial | 1 − e^(−ratio) |
| --- | --- | --- |
| 0.01 | 0.0174 | 0.0100 (polynomial is **74 % high**) |
| 0.5 | 0.3869 | 0.3935 |
| 4 | 0.9843 | 0.9817 |
| 5 | 0.9814 | 0.9933 (polynomial **decreases** between 4 and 5) |

The closed form removes the need for the polynomial, the hard-coded coefficients, and the 0.002 and 5 cutoffs. It also makes `prob_detection.py` a validation script rather than a dependency. Note that "probability that bubbles overlap" is a simplification and not detection itself, as `09_galaxy_simulator_project_concept.md:226` points out.

🟢 **C-9:** The Content Security Policy allows `'unsafe-inline'` scripts (`__init__.py:29`), which removes most of the CSP's XSS protection. Talisman supports nonces (`content_security_policy_nonce_in=['script-src']`). Add `nonce="{{ csp_nonce() }}"` to the two inline `<script>` blocks in `base.html`.

🟢 **C-10:** `run.py:4-5` appends `src` to `sys.path` and then imports `src.fermi_paradox`. `__init__.py` then imports `fermi_paradox.config.settings`, so the package `__init__` runs under two module names. Use `from fermi_paradox import create_app`, or better, make the package installable (see S-1) and drop the `sys.path` hack.

🟢 **C-11: Template defects in `base.html`.**

- The favicon is linked twice. The second link (`:92`, `static/images/favicon.ico`) returns **404**.
- `style.css` is loaded twice (`:96` and `:105`). The first copy loads *before* Bootstrap, so Bootstrap overrides it.
- `{{ current_year or 2025 }}` (`:164`) always shows 2025 because no context processor provides `current_year`.
- `<div>` elements are direct children of `<ul class="navbar-nav">` (`:134-149`), which is invalid HTML.
- "Galaxy Simulator" and "Probability Detection" links on the home page and in the nav point to `#`.

🟢 **C-12:** Logging defaults disagree. `Config.LOG_LEVEL` defaults to `INFO` (`settings.py:29`), but the logger itself defaults to `DEBUG` (`settings.py:58`). `Config.LOG_LEVEL` is never applied.

### 4.2 Efficiency

🟠 **E-1: `prob_detection.py` is pure-Python and slow.** It makes about **122.6 million** `randint` calls in nested Python loops (51 civilization counts × 1,000 trials × up to 5,002 draws), followed by `Counter` work, so it takes minutes. Options:

- **Best:** use the closed form above (C-8). The cost becomes negligible.
- **To keep the Monte Carlo for validation:** vectorize it with NumPy:

  ```python
  rng = np.random.default_rng(seed)
  locs = rng.integers(0, V, size=(TRIALS, n))
  counts = np.apply_along_axis(np.bincount, 1, locs, minlength=V)  # or a flat bincount with offsets
  ```

  This is roughly 100× faster, and seeding it satisfies the reproducibility requirement in the docs.

🟢 **E-2:** `galaxy_simulator.py` imports NumPy only for `np.pi` (use `math.pi`). It also draws each star with a separate Tk canvas call. That is fine for Tk, but a web version will need server-side batch rendering (NumPy arrays plus matplotlib/Plotly) or client-side rendering.

🟢 **E-3:** Heavy and dev-only packages are in the runtime `requirements.txt`. Of 129 pinned packages, the app needs about 10 (Flask, Flask-WTF, WTForms, flask-talisman, gunicorn, python-dotenv, plus transitive dependencies). The file also ships all of Jupyter/JupyterLab, ipykernel, nbconvert, pandas, matplotlib, scipy, sympy, pytest, ruff, `pandas-stubs`, `types-*`, and **`nose`** (unmaintained and broken on Python ≥ 3.10). This inflates the Heroku slug and build time. The Bayesian docs recommend PyMC, ArviZ, and Plotly, but none of them are listed. See S-1.

🟢 **E-4:** `matplotlib.use('TkAgg')` at import (`prob_detection.py:5`) forces a GUI backend. This fails on headless servers.

### 4.3 Structure and maintainability

🟠 **S-1: Add a `pyproject.toml`** (already promised in the architecture docs). Use it to:

- Make `fermi_paradox` installable (`pip install -e .`), which removes the `run.py` `sys.path` hack and the `pytest.ini` `pythonpath = src` workaround.
- Split dependencies into `[project.dependencies]` (runtime), `[project.optional-dependencies] dev` (pytest, ruff, bs4, lxml), `notebooks` (jupyter, matplotlib), and later `science` (numpy, scipy, pymc).
- Generate a slim `requirements.txt` for Heroku from the runtime set.

🟠 **S-2: Convert scripts into importable modules.** Separate pure computation from presentation:

- `core/detection_probability.py`: pure functions (`overlap_probability(n_civs, n_volumes)`, `simulate_overlap(…, rng)`), with no I/O at import time
- `core/galaxy_model.py`: pure coordinate generation (spiral arms, haze) that returns arrays
- `research/` or `scripts/`: the Tk renderer and the plotting and fit code, behind `if __name__ == "__main__":`

The plotting side can later move to the planned `core/visualization.py`.

🟠 **S-3: Route layer cleanup.** `api/routes.py`

- Rename the blueprint. It is named `api` and mounted under `/api/…`, but it serves **HTML pages**, not an API. When JSON endpoints arrive (Bayesian Drake per `00_github issues.md` §03.02), the naming will collide. Suggested: a `pages` blueprint at `/drake`, `/drake/edit`, and an `api` blueprint for JSON.
- The prefill and collect code in `edit_drake_params` (`:36-55`) repeats each parameter by hand. Replace it with `DrakeForm(data=DEFAULT_DRAKE_PARAMS)` and `params = {k: form[k].data for k in DEFAULT_DRAKE_PARAMS}`.
- `name = None` (`:34`) is passed to the template but never used.
- The `submit = SubmitField("Recalculate")` in `drake_form.py:22` is never rendered; the template uses its own "Update Parameters" button.
- `edit-drake.html` repeats the same 6-line block for 7 fields. Loop over `form` (excluding `csrf_token`).

🟢 **S-4: Configuration hygiene.**

- Move the parameter metadata (label, symbol, bounds, default, justification) into one structure in `config/drake_number_params.py`. The form, both templates, and the docs table can be generated from it. That removes the D-2 and C-7 kind of drift.
- Choose the config by a dedicated variable (e.g. `APP_ENV`, which `.env.example` already defines). `FLASK_ENV` was deprecated in Flask 2.2/2.3.
- Delete the unused `.env.example` keys, or mark them clearly as reserved.

🟢 **S-5: Code hygiene.**

- `main.py`: remove the duplicated `__main__` block and the archived-calculation string (move them to `docs/06_development_notes/` if they are worth keeping).
- Fix docstring paths in the tests: they say `tests/test_api_routes.py` and `tests/test_drake_equation.py`, but the files live in subfolders.
- Fix typos: `Calulates` (`drake_equation.py:10`), `calcuate` (`routes.py:62`), `Dectection` (`prob_detection.py:54`), `logrithmic` and `appied` (`galaxy_simulator.py`).
- Move the notebook in `src/fermi_paradox/bayesian_playground/` to `research/notebooks/` (per the architecture docs) so it is not part of the deployable package.

### 4.4 Tests and CI

🟠 **T-1: Tests are weak in specific ways.**

- **They assert type and range, not values.** `test_calculate_drake_number` only checks `> 0`. Add an exact known-answer test, e.g. Drake 1961 inputs should give 7.875×10⁶ and Drake 2017 inputs 15.6×10⁶ (`pytest.approx`). These are the documented reference values, and they would have caught D-1.
- **`test_drake_route_post` does not check that recalculation happened.** It also mutates global state (C-1).
- **No coverage for** `/api/edit-drake` (valid submit, invalid submit, zero values, CSRF), the non-numeric input case, or anything in `galaxy_simulator.py` and `prob_detection.py`.
- **Inconsistent sanity bounds:** `< 1e12` (`test_drake_equation.py:32`) vs. `< 1e9` (`:50`).
- **Tests run under `DevelopmentConfig`.** The fixture calls `create_app()`, which selects `DevelopmentConfig` (`DEBUG=True`), and sets `TESTING` afterwards. The test client works only because `DEBUG=True` disables Talisman's HTTPS redirect. **Verified:** with `DEBUG=False`, `GET /` returns 302. Pass `TestingConfig` explicitly and set `force_https` from config so tests reflect production behavior.

🟢 **T-2: CI improvements.**

- Add `dev` to the branch triggers.
- Upload a readable coverage report (`--cov-report=xml`) instead of the binary `.coverage` file.
- Replace the static README badges with the live GitHub Actions badge.

---

## 5. Prioritized Action List

| # | Action | Fixes |
| --- | --- | --- |
| 1 | Copy (don't alias) `DEFAULT_DRAKE_PARAMS` in routes, or remove `POST` from `/api/drake` | C-1, C-2 |
| 2 | Confirm `L_2017` against the source, remove the `/ 2`, and update the code, the UI, and `02_drake_number_documentation.md` together | D-1, D-2, C-3 |
| 3 | Switch `DataRequired` to `InputRequired`; fail fast on a missing production `SECRET_KEY` | C-5, C-6 |
| 4 | Add known-answer Drake tests (1961 → 7.875e6, 2017 → 15.6e6) and edit-route tests | T-1 |
| 5 | Split architecture docs into "Current" and "Planned"; fix README claims, badges, tree, and install steps | §2.1, §2.3 |
| 6 | Make `01_roadmap.md` the single master roadmap that includes Bayesian Drake, the hypothesis model, galaxy simulator, and time dilation; link sub-plans | X-1 |
| 7 | Settle file and template names (`bayesian_drake.py`, the hypothesis engine name, the template folder) and the issue 01.01/01.02 status, then update every doc that refers to them | X-2 – X-5 |
| 8 | Reconcile prior-set definitions and the forward-MC vs. inference wording; change n_e's prior from Beta to log-normal or gamma | X-6, X-8, X-9 |
| 9 | Refactor `galaxy_simulator.py` and `prob_detection.py` into pure, importable modules; replace the polynomial with the closed form; seed the RNG | C-4, C-8, E-1, S-2 |
| 10 | Add `pyproject.toml` and split runtime and dev dependencies | S-1, E-3 |
| 11 | Update `02_structure_description.md` to the new docs layout; fix the `..` and `../../` path artifacts; deduplicate the Bayesian parameter docs | X-12, X-14 |
| 12 | Fix the time-dilation figure (400 → ~4,470 years) and the editorial issues | X-15 |
| 13 | Clean up `base.html` (favicon, CSS, year, nav HTML) and add CSP nonces | C-9, C-11 |

---

## 6. What Is in Good Shape

- The app-factory pattern (`create_app`) with blueprint registration and environment-selected config is a sound foundation.
- The deterministic Drake core is pure and framework-independent, as the architecture intends.
- Security headers through Talisman, with HSTS preload, are already in place.
- Lint (ruff) and tests run in CI, and all of them currently pass.
- `09_galaxy_simulator_project_concept.md` is a strong spec: explicit assumptions, verification cases with known answers, interval conventions, and honest limitations. Using it as the template for the Bayesian Drake spec would resolve many of the conflicts in §3.
- The scientific references and the γ table in the time-dilation doc check out numerically. So do the Drake 1961 and 2017 N values and the signal-delay figures.
