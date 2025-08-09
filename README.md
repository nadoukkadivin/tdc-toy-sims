# tdc-toy-sims
# toy sims for wip tidal drift communication (tdc) — example 1 (`tdc_eg1_toysim.py`)

### **What is this?**
This repository demonstrates a quantitative comparison between classic biophysical modelling (**Hodgkin-Huxley + Langevin**) and a streamlined **Tidal-drift communication (TDC)** formulation for simulating bioelectronic hybrid signal propagation under different thermal conditions.

## **Contents**

- **`tdc_eg1_toysim.py`:** Python code for running both baseline (HH+Langevin) and TDC models, automated benchmarking and figure generation.
- **`README.md`:** This documentation outlines the context, validation protocol, result interpretation and references.
- (optional) **`.pdf`** and **`.png`** figures showing signal propagation and result metrics are auto-saved on each run.

## **Rationale**

- **Classic models (HH+Langevin):** Used for detailed single-neuron/hybrid circuit simulation, typically requiring 7-10+ physical parameters for complex, noisy or sensor hybrid scenarios;
- **TDC (Tidal-drift communication) model:** Condenses drift, entropic noise, and residual signalling into a compact, low-parametric equation, reducing parameter count by ~50% without loss of essential signal dynamics, especially in long-chain or sensor hybrids.

## **Key improvements & validation metrics**

- **Biophysical grounding:**
- **AP width / τ_d = 1.5ms:** Matches mammalian experimental data;
- **Temp scaling (Q10=3):** Standard for ion channel kinetics;
- **Noise term:** Realistic Johnson–Nyquist noise, scales with √T.

**TDC parameter mapping:**
| parameter | meaning                                                      | example value   |
|-----------|--------------------------------------------------------------|-----------------|
| Dr        | drift ratio (τ_coupling / τ_decay, e.g., NMDA/AMPA ratio)    | 0.3             |
| S         | entropy scaling (∝√kB*T*Cm, empirically tuned)               | 0.15            |
| I         | signal amplitude / persistence                               | 30 mV           |
| r0        | residue amplitude (hyperpolarization/“memory”)               | 5 mV            |
| α         | residue decay rate (1/50ms ~ Ca²⁺ decay timescale)           | 20 s⁻¹          |

**Validation protocol:**
- Simulate action potential (AP)-like signals using both HH+Langevin (10 param) and TDC (5 param) at 37°C (physiological) and 50°C (thermal stress);
- **Benchmark:** signal-to-noise ratio (SNR) calculated in the main post-AP window ( ms);
- **Criteria:** **1.** parameter reduction ≥50%; **2.** TDC delivers >2dB SNR gain over baseline at 50°C.

## **Expected results**

Parameter reduction: 50%
SNR room temp:
Baseline: 15.2 dB
TDC:      14.8 dB
SNR high temp (50°C):
Baseline: 8.7 dB
TDC:      12.1 dB

✅ Validation passed
Parameter reduction: 50%
High-temp SNR gain: 3.4 dB
Saved figures: tdc_vs_hh_high_temp_YYYYMMDD_HHMMSS.pdf, tdc_vs_hh_high_temp_YYYYMMDD_HHMMSS.png
```
- **Interpretation:** TDC delivers robust signal propagation with half the parameter count, even outperforming HH+Langevin under thermal stress.

## **How to run**

1. **Install dependencies:**  
   ```bash
   pip install numpy scipy matplotlib
   ```

2. **Execute toy simulation:**  
   ```bash
   python tdc_eg1_toysim.py
   ```
  SNR benchmarking and two plots (**`.pdf`/`.png`**) will be generated in the current directory.

3. **Exit codes:** 
- `0`: Validation passed (50% param reduction + >2dB SNR gain)
- `1`: Validation failed

## **References & parameter sources**

### **Biophysical models**
  - **Hodgkin & Huxley** (1952) “A quantitative description of membrane current and its application to conduction and excitation in nerve”, Journal of Physiology, 117(4) 500–544 https://pmc.ncbi.nlm.nih.gov/articles/PMC1392413/;
  - Gerstner et al (2014) **"Neuronal Dynamics: From Single Neurons to Networks and Models of Cognition"** (https://neuronaldynamics.epfl.ch/online/Ch2.S2.html);
  - Hille (2001) **"Ion Channels of Excitable Membranes"**, 3rd Edition, Sinauer Associates (https://archive.org/details/ionchannelsofexc0003hill); 
  - Yang & Zheng (2014) **“Temperature dependence of ion channel kinetics”**, Channels, 8(4) 308–321 (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2891698/); 
  - **Channel Noise and Johnson–Nyquist Theory**: Johnson (1928) “Thermal Agitation of Electricity in Conductors”, Physical Review, 32(1) 97–109 (https://web.mit.edu/dvp/Public/noise-paper.pdf);
  - Bertram (2021) **“Channel Noise in Neurons”** (https://www.math.fsu.edu/~bertram/course_papers/Fall21/channel_noise.pdf).

### **TDC formalism core**
  - Prigogine (1977) *Dissipative Structures in Energy and Matter*;  
  - Friston (2010) *Free-Energy Principle: Unified Brain Theory*;  
  - Current preprints: *Substrate-agnostic signalling framework* (contact author)
  - Parameter mapping:  NMDA/AMPA kinetics → Drift (Dr), Ca²⁺ decay timescales → Residue decay (α), Action potential physiology → Inertia (I).

### **Validation & benchmarking**
- **Goldman** (1943) “Potential, Impedance, and Rectification in Membranes.” Journal of General Physiology, 27(1), 37–60 (https://doi.org/10.1085/jgp.27.1.37);
- **Goldwyn & Shea-Brown** (2011) “The what and where of adding channel noise to the Hodgkin-Huxley equations”, Journal of Neurophysiology, 106(4), 2107–2118 (https://journals.physiology.org/doi/full/10.1152/jn.00686.2003); 
- **IEC 60601-2-78** (2023) 'Medical Electrical Equipment—Part 2-78: Particular requirements for basic safety and essential performance of medical electrical equipment for electrophysiological signal quality" (https://webstore.iec.ch/en/publication/31388).

  ### **Param legend**
| parameter   | source                       | value in code              |
|-------------|------------------------------|----------------------------|
| τ_d = 1.5ms | Mammalian AP duration        | `τ_d = 1.5e-3`             |
| Q₁₀ = 3     | Ion channel Q10 scaling      | `phi = 3.0**((T - 298)/10)`|
| α = 20 s⁻¹  | Ca²⁺ decay in synapses       | `alpha = 1 / 50e-3`        |

## **Reproducibility & validation**

- **Random seed fixed** for reproducibility.
- **Automated validations block:** assert param/SNR criteria (code output & exit code).
- **Output plots:** **Top:** room temp (37°C), baseline vs TDC; **Bottom:** 50°C stress test, baseline vs TDC.

## **Customization/extension**

- Adjust parameters in `tdc_biohybrid` or initial conditions to test new regimes;
- Adapt for long-chain or extended sensor/junction scenarios to mirror realistic bioelectronic hybrid devices;
- SNR, param reduction, and thermal resilience claims can be easily updated or extended for future benchmarks.

## **Contact**

For questions, bugs or collab: [Nadoukká Divin], [Rhythm and density], [nadoukkadivin@gmail.com].

### Sample figure output

Image: “Bioelectronic hybrid resilience” (insert sample_figure.png here) **Top**: 37°C comparison (baseline vs TDC) **Bottom**: 50°C stress test showing TDC's SNR advantage)
