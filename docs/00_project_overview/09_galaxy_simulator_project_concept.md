# Galaxy Simulator — Project Concept

**Project:** Fermi Paradox Project  
**Document status:** Proposed scope; implementation has not been verified or started through this document  
**Date:** November 1, 2026

## 1. Purpose

Develop a computational simulation that explores how the locations, emergence times, and detectable lifetimes of hypothetical technological civilizations influence opportunities for interstellar detection.

The simulator will extend the Fermi Paradox Project beyond aggregate Drake-equation estimates by introducing spatial separation, signal travel time, and temporal overlap.

**Central question:** Even if technological civilizations exist, do their locations and timing allow one to detect another?

The project is an independent learning and research-and-development exercise. Its results will be conditional on documented assumptions; they will not establish the actual prevalence of extraterrestrial life.

## 2. Scope options

| Version | What it models | Relative effort |
| --- | --- | --- |
| Synthetic galaxy | Locations of stars or representative planetary systems in a simplified Milky Way | Manageable starting point |
| Civilization and detection simulator | Civilizations emerging, transmitting, listening, and ceasing detectable activity | Substantial but practical personal project |
| Expansion simulator | Probes or settlements spreading between systems over time | More demanding extension |
| Gravitational galaxy simulator | Stellar motion under gravity, potentially including dark matter and gas | Separate, much larger computational physics project |

**Recommended initial scope:** A static synthetic galaxy combined with a civilization-emergence and signal-arrival model.

## 3. First milestone

Generate a static synthetic galaxy, assign hypothetical civilization emergence times and detectable lifetimes, and determine whether transmissions reach Earth during a specified listening window.

### Minimum deliverables

- A documented synthetic spatial population.
- Explicit Earth or Solar System coordinates within the model.
- Civilization emergence times and transmission intervals.
- A configurable Earth listening interval.
- Signal travel-time and interval-overlap calculations.
- A static visualization and a table of detection opportunities.
- Reproducible configuration and random seed.
- Verification against simple cases with known answers.

### Initial exclusions

- Gravitational N-body dynamics and stellar orbital motion.
- Gas dynamics, galaxy formation, and dark-matter evolution.
- Interstellar settlement and probe expansion.
- Detailed telescope or radio-receiver performance.
- A complete star-by-star reconstruction of the Milky Way.

## 4. Initial modeling assumptions

These are proposed simplifications to evaluate and document before implementation.

| Topic | Proposed treatment | Limitation |
| --- | --- | --- |
| Geometry | Two-dimensional static galaxy for the first version | Omits vertical structure and system motion |
| Spatial population | Synthetic systems generated from a documented distribution | Does not reproduce an observed stellar catalog |
| Emergence | Sample hypothetical civilization emergence times from a configurable model | Emergence rates and distributions are uncertain assumptions |
| Detectability | Assign a transmission start time and duration | Detectable activity is not necessarily the full biological lifetime |
| Listening | Specify receiver listening intervals separately | Being technologically active does not imply continuous listening |
| Signal propagation | Straight-line travel at light speed | Omits propagation losses and environmental effects initially |
| Detection reach | Optional fixed maximum distance | A scenario parameter rather than a physically complete sensitivity model |
| Detection event | Received transmission overlaps a listening interval and satisfies the simplified range rule | Represents an opportunity under the model, not guaranteed recognition |

A more detailed signal model could later include transmitter power, beam direction, frequency, receiver sensitivity, and observation schedules.

## 5. Signal timing

Use consistent units throughout. Light-years for distance and years for time make the propagation calculation straightforward: light travels one light-year per year.

For distance `d` and light speed `c`:

```text
travel_time = d / c
arrival_start = transmission_start + travel_time
arrival_end = transmission_end + travel_time
```

A detection opportunity exists when the arrival interval overlaps a receiver's listening interval, subject to the model's range and other detection assumptions.

For positive-duration intervals, a useful overlap test is:

```text
max(arrival_start, listening_start) < min(arrival_end, listening_end)
```

Document the boundary convention. The strict comparison above requires positive-duration overlap; an instantaneous boundary touch does not count.

### Finite transmissions

A finite transmission produces a traveling shell rather than a permanently filled expanding sphere. The shell's radial thickness is `c × transmission_duration`. In a two-dimensional visualization, its cross-section appears as an annulus.

A transmitter can cease activity before its signal reaches a listener. A listener can also emerge too late to receive a transmission that has already passed.

### Time boundaries

Specify whether the simulation includes transmissions emitted before the displayed observation period. Otherwise, initialization can artificially exclude signals already in transit.

## 6. Proposed components

| Component | Responsibility |
| --- | --- |
| Galaxy generator | Produce system coordinates from the chosen spatial model |
| Civilization model | Sample emergence times, transmission durations, and listening behavior |
| Signal model | Calculate distances, travel times, and reception intervals |
| Simulation engine | Evaluate events and record detection opportunities |
| Experiment runner | Repeat scenarios and summarize distributions |
| Visualization | Present the galaxy, timeline, and selected results |
| Documentation | Record sources, assumptions, units, limitations, and interpretation |

Keep the Python simulation independent of the website interface. Establish correct calculations and reproducible experiments before adding interactive graphics.

A full event-driven engine is optional for the first milestone: direct interval calculations may be sufficient for Earth-only reception.

## 7. Suggested conceptual data records

Exact schemas remain an implementation decision.

| Record | Example fields |
| --- | --- |
| System | System ID, coordinates, population interpretation |
| Civilization | Civilization ID, system ID, emergence time, transmission start/end, listening start/end |
| Scenario | Spatial assumptions, population size, time bounds, emergence parameters, range assumptions, random seed |
| Detection opportunity | Transmitter ID, receiver ID, distance, signal arrival interval, overlap duration |
| Run summary | Scenario ID, run ID, population counts, detection counts, defined outcome metrics |

State whether multiple technological civilizations may arise in the same system. A one-civilization-per-system rule is a modeling choice, not a physical fact.

## 8. Data requirements and population scaling

The initial version can use entirely synthetic data. Observational catalogs are not required to develop or verify the mechanics.

Sources will still be needed to justify any adopted Milky Way dimensions, spatial distributions, or other physical parameters. This concept document does not yet select or validate those values.

Define what each simulated point represents. Possible interpretations include:

- One explicitly modeled stellar system.
- One candidate system capable of hosting a hypothetical civilization.
- A representative sample of a larger population.

Detection statistics from a sampled population cannot automatically be interpreted as whole-galaxy results. Representative weights alone do not recreate omitted spatial relationships or detection events. Start with an explicitly defined modeled population and address scaling before making galaxy-wide claims.

## 9. Mathematical and technical preparation

The first version primarily requires:

- Probability distributions and Monte Carlo simulation.
- Coordinate systems and Euclidean distance.
- Time intervals and event logic.
- Reproducible random sampling.
- Sensitivity analysis and numerical verification.

Differential equations are not required for the static initial model. They become relevant if orbital motion is introduced later.

Earth-only reception requires approximately one distance calculation per transmitter. Evaluating all civilization pairs grows quadratically with population size; spatial searches or other pruning may become useful for larger experiments.

## 10. Phased development plan

### Phase 1 — Define and generate the synthetic population

- [ ] Define the scientific question and meaning of each simulated point.
- [ ] Choose units, coordinates, time bounds, and interval conventions.
- [ ] Select and document a simple spatial distribution.
- [ ] Generate a reproducible synthetic population.
- [ ] Plot system locations and the receiver position.

### Phase 2 — Implement Earth-directed reception calculations

- [ ] Define civilization emergence and transmission assumptions.
- [ ] Sample emergence times and transmission intervals.
- [ ] Define Earth's listening window.
- [ ] Calculate signal arrival intervals.
- [ ] Identify overlaps and apply the simplified range rule, if used.
- [ ] Produce a detection-opportunity table.
- [ ] Verify known-answer cases.

### Phase 3 — Run repeated experiments

- [ ] Repeat scenarios across independent random realizations.
- [ ] Summarize the fraction of runs with at least one Earth detection opportunity.
- [ ] Report detection-count distributions.
- [ ] Examine sensitivity to emergence rates, transmission durations, range assumptions, and listening windows.
- [ ] Report Monte Carlo sampling uncertainty separately from uncertainty in the physical assumptions.

### Phase 4 — Add website visualization

- [ ] Start with a two-dimensional map and time slider.
- [ ] Display transmitter activity and signal propagation consistently with the simulation.
- [ ] Explain controls and assumptions in plain language.
- [ ] Show results from repeated runs alongside individual realizations.
- [ ] Decide whether calculations run live or use precomputed results after reviewing the existing website architecture.

### Phase 5 — Evaluate extensions

- [ ] Civilization-to-civilization detection.
- [ ] Directional or intermittent transmissions.
- [ ] Receiver sensitivity and signal-power models.
- [ ] Three-dimensional galactic structure.
- [ ] Probe or settlement expansion.
- [ ] Orbital motion, if justified by the scenario and time span.

## 11. Verification cases

| Case | Expected behavior |
| --- | --- |
| Transmitter 1,000 light-years away | Arrival is delayed by 1,000 years |
| Transmission ends before reception | The signal can still arrive after the transmitter ceases activity |
| Arrival interval precedes listening | No detection opportunity |
| Arrival interval overlaps listening | Detection opportunity if other model conditions are satisfied |
| Intervals touch at one boundary only | Follow the documented endpoint rule; under positive-duration overlap, do not count |
| Transmitter outside a configured range limit | Excluded under that simplified detection rule |
| Repeated run with identical configuration and seed | Identical generated population and results within the supported execution environment |

These checks establish implementation consistency. They do not validate speculative civilization parameters as descriptions of reality.

## 12. Candidate outputs

- Number of modeled civilizations and transmitters.
- Number of Earth reception opportunities during a defined interval.
- Fraction of Monte Carlo runs with at least one reception opportunity.
- Distributions of counts and overlap durations.
- Conditional waiting times where detections occur, with no-detection runs reported separately.
- Sensitivity plots showing how outcomes depend on selected assumptions.

Use labels such as **modeled detection opportunity** rather than implying that geometric overlap alone guarantees a confirmed detection.

## 13. Planning estimate

These are rough personal-project estimates, not commitments. They depend on available time, scope, and the existing website architecture.

| Deliverable | Approximate effort |
| --- | --- |
| Static population and civilization assignment | A few focused weekends |
| Verified signal timing and repeated experiments | Several additional weekends |
| Polished interactive website feature | Potentially a few months of occasional work |

The modeling assumptions, verification, and interpretation deserve as much attention as the animation.

## 14. Publication opportunity

The first milestone could support an *After Hours Astrophysics* article exploring:

**If civilizations exist, why might their signals never overlap with our opportunity to listen?**

Explain the question, show a simple example, and distinguish physical propagation rules from hypothetical civilization assumptions. Readers should be able to follow the article without running code.

## 15. Next decision

Begin with a static two-dimensional synthetic population and Earth-only reception calculations. Establish reproducibility and known-answer checks before expanding the population model, building an event engine, or integrating the website.
