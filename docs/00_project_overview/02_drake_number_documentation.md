# Drake Number Calculation Documentation

This documentation provides an overview of the Drake number calculation process, including the parameters used in the calculation and their significance.

## Parameters

- `R_`: Average rate of star formation per year.
- `f_p`: Fraction of stars that have planets.
- `n_e`: Average number of planets per star that can support life.
- `f_l`: Fraction of planets that could support life that actually do.
- `f_i`: Fraction of planets with life that develop intelligent life.
- `f_c`: Fraction of intelligent civilizations that develop technology capable of interstellar communication.
- `L`: Expected lifetime of a technological civilization in years.

---

## Equation

The Drake Equation is given by:
\[
N = R^* \times f(p) \times n(e) \times f(l) \times f(i) \times f(c) \times L
\]

---

## Input Table

## 🧮 Drake Inputs Table

|  Parameter  | Description | Drake (1961) | Drake (2017) | Used in Model |
|:-----------:|:------------|:-------------:|:-------------:|:--------------:|
| **R_star** | Average rate of star formation in the galaxy (stars per year) | 1 | 3 | 2 |
|  **f(p)**   | Fraction of stars that have planetary systems | 0.35 | 1 | 0.8 |
|  **n(e)**   | Average number of planets per system that could support life | 3 | 0.2 | 0.2 |
|  **f(l)**   | Fraction of suitable planets where life actually develops | 1 | 0.13 | 0.5 |
|  **f(i)**   | Fraction of life-bearing planets where intelligent life evolves | 1 | 1 | 1 |
|  **f(c)**   | Fraction of intelligent civilizations that release detectable signals | 0.15 | 0.2 | 0.1 |
|    **L**    | Average lifetime (in years) that civilizations release detectable signals | 50×10⁶ | 1×10⁹ | 1,000 |
|    **N**    | Estimated number of detectable civilizations in the galaxy | 7.9×10⁶ | 15.6×10⁶ | — |

---

## 🧠 Parameter Justifications

Below are the reasoning and assumptions used to determine the “Used in Model” column for each parameter in the Drake Equation.

---

### **R\*** — Rate of Star Formation  

Current estimates suggest that approximately **1–3 new stars** form in the Milky Way each year.  
For this model, a midpoint value of **2 stars per year** is used.

---

### **f(p)** — Fraction of Stars with Planetary Systems  

Observations from missions such as **Kepler** indicate that most stars have planets, with estimates between **0.7 and 1.0**.  
A value of **1.0** is used for simplicity, assuming nearly all stars host planets.

---

### **n(e)** — Average Number of Habitable Planets per System  

Recent **exoplanet studies** suggest that between **0.1 and 0.2** planets per star could support life.  
A value of **0.2** is used to represent an optimistic but reasonable estimate.

---

### **f(l)** — Fraction of Habitable Planets Where Life Appears  

This parameter is **highly uncertain**. Some theories assume life will almost always develop when conditions are right (**f(l) = 1**), while others predict it’s extremely rare.  
A balanced value of **0.5** is used to reflect moderate optimism.

---

### **f(i)** — Fraction of Life-Bearing Planets that Develop Intelligence  

The development of intelligent life is another area of significant uncertainty.
The emergence of intelligent life remains **speculative**. Estimates range from extremely low to near certainty.  
This model uses **f(i) = 0.1** to represent a cautious assumption.

---

### **f(c)** — Fraction of Intelligent Civilizations that Develop Detectable Technology  

Even among intelligent civilizations, few may produce **detectable electromagnetic signals** or sustain them long enough to overlap with others.  
This model assumes **f(c) = 0.1**, suggesting a relatively small proportion develop and maintain technology capable of detection.

---

### **L** — Average Lifetime of Detectable Civilizations  

The longevity of technological civilizations is **highly speculative**.
If we assume civilizations release detectable signals for roughly **1,000 years**, then **L = 1,000**.  
For context, Earth has been transmitting detectable radio waves for about **124 years** (since around **1901**).  
This duration provides a frame of reference for a relatively short-lived technological phase on a cosmic timescale.

---

## References

- [Drake Equation](https://en.wikipedia.org/wiki/Drake_equation)
- [Fermi Paradox](https://en.wikipedia.org/wiki/Fermi_paradox)
- [SETI](https://en.wikipedia.org/wiki/Search_for_extraterrestrial_intelligence)
- [Carl Sagan](https://en.wikipedia.org/wiki/Carl_Sagan)
- [Frank Drake](https://en.wikipedia.org/wiki/Frank_Drake)

---

## Acknowledgments

This documentation was created with the support of the SETI Institute and the Carl Sagan Center for the Study of Life in the Universe.
