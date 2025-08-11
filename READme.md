# tdc-toy-sims

## toy sims for wip tidal drift communication (tdc) — example 3 (`tdc_geophy_bio.py`)

### **What is this?**
This example extends the Tidal‑drift communication (TDC) framework to **extreme-environment, geophysical–bio hybrid systems** such as hydrothermal vent electron transfer networks and geo‑bio sensor arrays.  
It benchmarks TDC against classical flux-based models using **Self‑Organized Criticality (SOC)** for event statistics and **Onsager reciprocal relations** for coupled heat/electron transport.

***

## **Contents**

- **`tdc_geophy_bio.py`** — Python code for simulating SOC avalanche events, Onsager flux coupling, mineralised mat residue dynamics, and TDC-based drift ratio adaptation.
- **`README.md`** — This documentation: context, physics mapping, protocols, and references.
- **Output figures**: Multi-panel `.pdf` and `.png` saved automatically (flux/efficiency, temperature, residues/Dr, SOC distribution).

## **Scientific rationale**

- **Challenge:**  
  Real‑world geo‑bio hybrids (vent microbes, mineral mats, electrode arrays) must operate under **extreme temperature/pressure** with intermittent gradients. Classical models need large parameter sets (~10+) to track flux, delay, and renewal processes; they often fail beyond ~500 bar, > 300 °C.
- **TDC approach:**  
  Uses **Dr** and a minimal set of substrate‑agnostic parameters to unify SOC criticality (event avalanche statistics) and Onsager flux gradients into one framework, cutting parameter count by ~20–40 %.
- **Core novelty:**  
  - SOC exponent stability at extremes  
  - Drift ratio scaling with P/T for predictive coherence  
  - Residue terms tracking slow mineral mat renewal (tidal cycles, hours–days)

## **Key features & validation metrics**

**Physics incorporated:**
- **SOC:** Bak–Tang–Wiesenfeld cellular automaton, avalanche size exponent τ ≈ 4.0
- **Onsager fluxes:** L\_ij coefficients for coupled heat/electron transport in mineral–microbe systems
- **Residue model:**  
  $$ r(t) = r_0 e^{-\alpha t} + \beta \sin(\omega t) $$  
  α ≈ 1 × 10⁻⁴ s⁻¹ (slow decay), β = 0.4, ω from tidal cycle (12 h period)
- **TDC Dr:** τ_coupling ≈ 1 h, τ_decay ≈ 20 min → Dr ≈ 3.0

**Parameter mapping (from code):**

| parameter | description                            | value in code      |
|-----------|----------------------------------------|--------------------|
| **Dr**    | τ_coupling / τ_decay                   | 3.0                |
| **S**     | Thermal/flux entropy scaling k\_B lnΩ  | ~0.4 Ω from vent turbulence |
| **r₀**    | Base residue amplitude                 | 0.35               |
| **α**     | Residue decay coefficient              | 1 × 10⁻⁴ s⁻¹       |
| **β**     | Renewal amplitude                      | 0.4                 |
| **ω**     | Renewal cycle frequency (tidal)        | 2π / 12 h           |

## **Validation protocol**

- **Benchmark:**  
  - SOC exponent τ calculated from avalanche size distribution (target: 3.8 – 4.2)  
  - Mean **EET efficiency** > 50 % and never < 30 % in run window  
  - Parameter reduction vs 10‑param baseline: ≥ 20–40 % fewer params
- **Criteria:**  
  - TDC maintains SOC exponent stability and ≥ 50 % EET at most extreme simulated conditions where baseline fails (> 500 bar or > 300 °C instability).  
  - All plots auto‑saved with a timestamp.

## **Expected results**

Example output:
```
=== Running simulation at 350 bar ===
SOC exponent τ = 4.05
Mean EET efficiency = 0.63 (PASS)
Parameter reduction = 30 %
Validation: PASS

Files saved: geophy_bio_hybrid_350bar_YYYYMMDD_HHMMSS.pdf/png
```

- **Interpretation:**  
  TDC matches SOC statistics and maintains high EET efficiency with a reduced parameter set; baseline models lose criticality and efficiency under the same conditions.

## **How to run**

1. **Install dependencies:**
   ```bash
   pip install numpy matplotlib scipy
   ```

2. **Run the simulation:**
   ```bash
   python tdc_geophy_bio.py
   ```
   Output SOC/EET metrics and saved plots appear in the working directory.

3. **Exit codes:**
   - `0`: Validation passed  
   - `1`: Validation failed

## **References & parameter sources**

- **Self‑Organized Criticality:** Bak, Tang & Wiesenfeld (1987), *Phys. Rev. Lett.* 59: 381–384  
- **Onsager relations:** Onsager, L. (1931), *Phys. Rev.* 37: 405–426  
- **Geochemical/biological coupling:** *Geophys. J. Int.* (2024), mineral–microbe Onsager coefficients  
- **EET in vent systems:** JACS studies on electroactive biofilms, 60–70 % efficiencies for hybrids  
- USGS Yellowstone earthquake swarm data  
- MetaSoil microbial datasets

## **Parameter legend**

| Symbol | Description                         | Value in code       |
|--------|-------------------------------------|---------------------|
| α      | Residue decay rate                  | 1 × 10⁻⁴ s⁻¹        |
| β      | Renewal amplitude                   | 0.4                 |
| ω      | Renewal cycle frequency (tidal)     | 2π / (12 h)         |
| L\_ij  | Onsager coefficients                | see ONSAGER\_COEFFS |
| τ\_d   | SOC & TDC decay time constants      | domain‑specific     |

## **Reproducibility & validation summary**

- Fixed seed for reproducibility.
- SOC analysis performed with log–log fit.
- EET and SOC exponent thresholds validated automatically.
- Environmental ranges: P = 200–500 bar, T = 100–300 °C.

## **Customization/extension**

- Swap SOC grid/threshold for other criticality models.
- Update Onsager L\_ij coefficients for new environments.
- Inject real field datasets instead of synthetic gradients.
- Extend for multi‑node geo‑bio sensor network simulation.

## **Contact**

For scientific queries, bugs, or collaboration: [Nadoukka Divin], [Rhythm and Density], [nadoukkadivin@gmail.com]

### **Sample figure output**

_Image: “Geo–bio hybrid criticality resilience” (insert `eg3_sample_figure.png` here)_

- **Top panel:** Electron flux & EET efficiency over time  
- **2nd panel:** Temperature profile under pressure  
- **3rd panel:** TDC drift ratio vs residue cycle  
- **Bottom panel:** SOC avalanche size distribution & power law fit
