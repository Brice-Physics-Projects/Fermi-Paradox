# 🌌 Fermi Paradox — Galactic Civilization Detection Model

This document explores the **probability of one advanced galactic civilization detecting another’s radio transmissions**, using the **Drake Equation** and a simulated Milky Way visualization.

---

## 🎯 Objective

Estimate the probability that, given a certain number of transmitting civilizations and the average size of their radio “bubbles,” one civilization’s radio signals would be detected by another.

As perspective, Earth’s current **radio bubble** is plotted on a **2D graphical representation of the Milky Way**.

---

## 🧩 Strategy

1. **Estimate the number of transmitting civilizations** using the **Drake Equation**.  
2. **Choose a range of radio bubble sizes** (distance signals travel).  
3. **Generate a formula** to estimate the probability of one civilization detecting another.  
4. **Build a graphical model** of the Milky Way and visualize Earth’s radio emission bubble.

---

## 🧮 The Drake Equation

\[
N = R^* \times f(p) \times n(e) \times f(l) \times f(i) \times f(c) \times L
\]

Where:

| Symbol | Description |
|:-------:|:------------|
| **N** | Number of civilizations whose electromagnetic emissions are detectable |
| **R\*** | Average rate of star formation in the galaxy (new stars per year) |
| **f(p)** | Fraction of stars with planetary systems |
| **n(e)** | Average number of planets per system that could support life |
| **f(l)** | Fraction of suitable planets where life actually develops |
| **f(i)** | Fraction of life-bearing planets that evolve intelligent life |
| **f(c)** | Fraction of intelligent civilizations that release detectable signals |
| **L** | Length of time (in years) that civilizations release detectable signals |

> **Note:**  
> Recent studies suggest that between **10% and 40% of planets** may be suitable for *some form* of life.

---

## 📊 Drake Equation Input Parameters

| Parameter | Drake (1961) | Drake (2017) | Used in Model |
|:----------:|:-------------:|:-------------:|:--------------:|
| R\* | 1 | 3 | — |
| f(p) | 0.35 | 1 | — |
| n(e) | 3 | 0.2 | — |
| f(l) | 1 | 0.13 | — |
| f(i) | 1 | 1 | — |
| f(c) | 0.15 | 0.2 | — |
| L | 50×10⁶ | 1×10⁹ | — |
| **N** | 7.9×10⁶ | 15.6×10⁶ | — |

---

## 🌠 Model Output (Planned)

- Simulated galaxy plot (2D view)  
- Earth’s current radio emission radius (~100 light-years)  
- Overlay of randomly distributed civilizations and their respective radio bubbles  
- Computed probability of overlap between radio bubbles

---

## 🧠 Notes

This model combines **probabilistic reasoning, astrophysics, and visualization** to illustrate the rarity — or potential abundance — of detectable civilizations.  
While largely *impractical*, the simulation aims to provoke curiosity about our place in the galaxy and the detectability limits of our own radio footprint.

---

>**“If there are billions of stars and countless worlds, where is everybody?” — Enrico Fermi**
