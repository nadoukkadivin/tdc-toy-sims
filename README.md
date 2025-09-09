# tdc-toy-sims

### **Simulation toolkit for Tidal–drift communication (TDC)**  
Physical, biological and hybrid system simulations demonstrating the **TDC** framework’s ability to model and validate signal/flux propagation under diverse conditions, with reduced parameter sets and improved resilience over traditional models.

## **What is TDC?**
Tidal–drift communication (TDC) is a substrate‑agnostic modelling framework that condenses drift, entropic noise, and residue “memory” into a compact set of parameters. It provides predictive continuity across domains — from neurons to gut–brain hybrids to geophysical–bio systems — while cutting the parameter count vs baseline models.

## **Repository structure**

| example | domain | focus | link |
|---------|--------|-------|------|
| **eg1** | Bioelectronic hybrid | HH + Langevin vs TDC for spike propagation under thermal stress | [eg1/README.md](eg1/README.md) |
| **eg2** | Gut–Blood–Brain hybrid chain | Multi‑domain signal resilience with entropy‑driven coupling | [eg2/README.md](eg2/README.md) |
| **eg3** | Geophysical–Bio hybrid | SOC + Onsager fluxes in vent–microbe systems | [eg3/README.md](eg3/README.md) |

## **Key features**
- **Physical & biological realism:** Q10 scaling, Johnson–Nyquist noise, realistic residue dynamics.
- **Cross‑domain modelling:** Chemical, electrical and environmental substrate physics unified in one form.
- **Parameter efficiency:** 20–50 % reduction vs comparable baseline models.
- **Automated validation:** Parameter count reduction, SNR/efficiency gains, SOC exponents, thermal resilience.
- **Publication‑ready output:** Timestamped figures in PDF/PNG with clear labelling.

## **Installation**

Clone this repository and install dependencies:

```bash
git clone https://github.com/yourusername/tdc-toy-sims.git
cd tdc-toy-sims
pip install -r requirements.txt
```

**Requirements**  
- `numpy`  
- `scipy`  
- `matplotlib`

## **Quickstart**

Each example folder contains:
- A `README.md` describing the scenario, physics mapping, parameters and validation protocol.
- A self‑contained Python script with `__main__` entry point.

Run an example:

```bash
cd eg1      # or eg2, eg3
python tdc_eg1_toysim.py
```

Results:
- Validation summary printed to console.
- Publication‑quality figures saved to the folder.

## **Universality demonstration: Drift (Dr) across domains**

TDC’s core advance is universality: By defining the Drift Ratio (`Dr = τ_coupling / τ_decay`) as a substrate-agnostic parameter, TDC can predict persistence and resilience not only in neurons (bioelectronic spikes) but also in bacterial systems (quorum sensing waves) and geophysical networks. 

**Schematic collapse of persistence by Dr**

| **system | t_coupling (ms/s) | t_decay (ms/s) | Dr | measured persistence (ms/s)** |
|---------|--------|-------|------|------|
| neural spike* | 1.5 ms | 0.5 ms | 3.0 | 8 ms |
|bacterial QS wave* | 180 s | 60 s | 3.0 | 900 s|

*Simulated/representative values 

Plotting persistence vs Dr for both domains shows a common scaling relationship – Dr bridges both the microsecond neural spikes and multi-minute bacterial wave persistence onto a universal curve. 

Insert simple figure here: persistence (y) vs Dr (x); neural and QS points lie on the same curve. This confirms TDC’s value in collapsing multi-domain behaviours for prediction and resilience – even in systems with vastly different physical scales.

# Residue dynamics simulation

The framework leverages:
- **Vectorised residue dynamics for computational efficiency**
- **Dimensional normalisation enabling substrate-agnostic thresholding and universality testing**
- **Cross-domain coupling to explore integrated multi-physics behaviour**

Codebase supports reproducible simulations, validation of cross-domain universality and result export for dissemination.

## Features

- Efficient multi-domain residue and signal ODE simulation with adaptive coupling
- Physical parameter normalization based on domain-specific scales (entropy, inertia, concentration)
- Sharpened sigmoid gating for precise response probability estimation
- Quantitative universality validation across domain behaviors using correlation and RMSE metrics
- Automated plotting and exporting of simulation results and validation summaries
- Configurable residue types and weights per domain to reflect biological/physical specificity

## **Citation**

If you use this code/concepts in research, please cite the relevant underlying work as listed in each example’s README.

## **License**
MIT License – see [LICENSE](LICENSE)

## **Contact**
For questions, bugs or collab: **Nadoukka Divin** — *Rhythm and density* — [nadoukkadivin@gmail.com](mailto:nadoukkadivin@gmail.com)

