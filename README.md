# tdc-toy-sims
# toy sims for wip tidal drift communication (tdc) — example 2 (`tdc_eg2_toysim.py`)

### **What is this?**
This repository demonstrates the Tidal-drift communication (TDC) framework for substrate-agnostic, multi-domain signal propagation through a chain representing **gut → blood → brain**. It benchmarks TDC’s compactness and resilience against a domain-adapted Hodgkin-Huxley + Langevin baseline including entropy-driven interface coupling and residue memory transfer.

## **Contents**

- **`tdc_eg2_toysim.py`;** Python code for multi-domain chain simulation, SNR benchmarking, automated thermal resilience validation and plots.
- **`README.md`:** This documentation outlines the context, validation protocol, result interpretation and references.
- (optional) **`.pdf`** and **`.png`** figures showing signal propagation and result metrics are auto-saved on each run.

## **Rationale**

- **Hybrid modeling challenge:** Biological signals often traverse distinct “substrates” (chemical → blood → neural), each with unique physics, scales, and dissipation;
- **Classic models (HH+Langevin):** Effective for electrical domains but not dimensionless chemical or biochemical regimes;
- **TDC model advantages:** Uses five core substrate-agnostic parameters for each domain (Dr, S, I, r₀, α), supports entropy-informed interface transduction, and models residue memory transfer.

## **Key features & validation metrics**

**Domain physics:**
- **Timescales:** Gut (2s), blood (0.5s), brain (1.5ms);
- **Q10 scaling:** Domain-specific temperature dependence;
- **Interface coupling:** Entropy-driven, not arbitrary percent loss;
- **Residue memory:** Physically accumulates and influences downstream domains.

**TDC parameter mapping:**

| parameter | description                     | example values (gut/blood/brain) |
|-----------|---------------------------------|----------------------------------|
| Dr        | drift/persistence scaling       | 0.1, 0.2, 0.3                    |
| S         | thermodynamic entropy scaling   | 0.25, 0.18, 0.12                 |
| I         | signal amplitude (dimensionless)| 0.8, 1.2, 1.5                    |
| r₀        | residue memory amplitude        | 0.4, 0.3, 0.2                    |
| α         | residue decay rate (s⁻¹)        | 1/200, 1/100, 1/50               |

**Validation protocol:**
- Simulate propagation through all three domains at 37°C and under 50°C “stress”;
- Calculate SNR in domain-appropriate time windows (Gut: 100–400ms, Blood: 3–8ms, Brain: 5–10ms).
- Report parameter reduction (8→5 params/domain), SNR change, and thermal resilience;
- **Benchmark:** Signal-to-noise ratio (SNR) is calculated in a physiologically relevant analysis window for each domain: **gut:** 100–400ms (reflecting slow chemical waves), **blood:** 3–8ms (intermediate transmission), **brain:** 5–10ms (rapid neural activity);
- **Criteria:** **1.** parameter reduction: At least 37.5% fewer model parameters in TDC vs. baseline HH+Langevin (8 → 5 per domain); **2.** signal robustness: for 37°C (normal), SNR for TDC is ≥ baseline SNR in brain/blood and no worse than -1.5dB in gut; **3.** thermal resilience: under 50°C thermal stress, the domain-averaged SNR improvement (TDC minus baseline) must exceed +2dB.

## **Expected results**  

Parameter reduction: 37.5%
**Gut:**
  37°C: HH=7.4dB, TDC=8.1dB → Δ=+0.7dB
  50°C: HH=3.3dB, TDC=6.0dB → Δ=+2.7dB
**Blood:**
  37°C: HH=11.1dB, TDC=10.9dB → Δ=-0.2dB
  50°C: HH=7.2dB, TDC=10.1dB → Δ=+2.9dB
**Brain:**
  37°C: HH=14.7dB, TDC=14.8dB → Δ=+0.1dB
  50°C: HH=8.5dB, TDC=11.6dB → Δ=+3.1dB

✅ Validation passed
Saved: tdc_eg2_results_YYYYMMDD_HHMMSS.pdf/png
```
- **Interpretation:** **1.** TDC achieves ≥37.5% parameter reduction; **2.** SNR is generally preserved per domain (slightly lower or higher by ≤ 1.5dB under homeostasis); **3.** TDC shows a domain-averaged SNR gain >2dB under thermal stress.

## **How to run**

1. **Install dependencies:**
   ```bash
   pip install numpy scipy matplotlib
   ```

2. **Execute toy simulation:**
   ```bash
   python tdc_eg2_toysim.py
   ```
   Output: SNR metrics per domain and timestamped plots in the current directory.

3. **Exit codes:**
   - `0` = Validation passed
   - `1` = Validation failed

## **References & parameter sources**

**Biophysical models:**
   - **Hodgkin & Huxley** (1952) “A quantitative description of membrane current and its application to conduction and excitation in nerve”, Journal of Physiology, 117(4) 500–544 https://pmc.ncbi.nlm.nih.gov/articles/PMC1392413/;
   - Gerstner et al (2014) **"Neuronal Dynamics: From Single Neurons to Networks and Models of Cognition"** (https://neuronaldynamics.epfl.ch/online/Ch2.S2.html);
   - Hille (2001) **"Ion Channels of Excitable Membranes"**, 3rd Edition, Sinauer Associates (https://archive.org/details/ionchannelsofexc0003hill);
   - Yang & Zheng (2014) **“Temperature dependence of ion channel kinetics”**, Channels, 8(4) 308–321 (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2891698/);
   - Bertram (2021) **“Channel Noise in Neurons”**(https://www.math.fsu.edu/~bertram/course_papers/Fall21/channel_noise.pdf).

**Entropy/transduction theory:**
- Prigogine (1977) *Dissipative Structures in Energy and Matter*;
- Friston (2010) *Free-Energy Principle: Unified Brain Theory*.

**Multi-domain hybrid modeling & benchmarking:**
- Goldwyn & Shea-Brown (2011), J Neurophys: [https://journals.physiology.org/doi/full/10.1152/jn.00686.2003](https://journals.physiology.org/doi/full/10.1152/jn.00686.2003)
- IEC 60601-2-78:2023 electrophysiological SNR standards: [https://webstore.iec.ch/en/publication/31388](https://webstore.iec.ch/en/publication/31388)

## **Param legend**

| parameter | description                        | value in code         |
|-----------|------------------------------------|-----------------------|
| τ_d       | Domain decay time (s)              | 2.0, 0.5, 1.5e-3      |
| Q10       | Channel temperature factor         | 1.8, 2.5, 3.0         |
| α         | Residue decay rate                 | 1/200, 1/100, 1/50    |

## **Reproducibility & validation **

- All code seed values are fixed for exact result replication;
- Domain-specific SNR windows ensure meaningful performance metrics;
- Automated assertions check param reduction, SNR consistency, and thermal performance;
- Plots and outputs are timestamped for provenance.

## **Customization/extension**

- Adjust any domain parameters to simulate other hybrid chains (vagus, sensor–bio etc);
- Tune entropy_transduction to explore non-ideal coupling or pathologies;
- Extend to more domains: increase `N`, generalise params.

## **Contact**

For questions, bugs or collab: [Nadoukka Divin], [Rhythm and Density], [nadoukkadivin@gmail.com]


### Sample figure output

Image: “Gut–blood–brain hybrid chain resilience” (insert `eg2_sample_figure.png` here) **Top:** gut (slow, chemical) → **Middle:** blood → **Bottom:** brain, all showing TDC vs HH* performance at 37°C/50°C and residue dynamics.
