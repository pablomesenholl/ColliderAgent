# Dilepton invariant mass at 14 TeV

## Run info

Run: `dy_ll_14tev_50k_run2`, 2026-10-05.

## Task and outcome

Generated 50,000 SM leading-order parton-level proton–proton events and plotted
the combined electron and muon dilepton invariant mass. The cross section with
the generation cuts is 1420.489 ± 1.331787 pb (integration uncertainty).
The plot covers 50–200 GeV in 2 GeV bins; 49,918 events are in this range and
82 are above it. There are 24,840 electron and 25,160 muon events.

## Execution

1. The pipeline orchestrator delegated generation to the MadGraph simulator.
   Corrected Magnus blueprint registrations were used. Compile job
   `a61dd46775bace78` and launch job `cf4b2c26c3254508` succeeded.
2. Direct Python LHE analysis calculated invariant masses, without a separate
   MadAnalysis run. All events passed checks of beam settings, final-state
   multiplicity, charge/flavor, finite momenta, mass shells, four-momentum
   conservation, generation cuts, actual event count and weight convention.
3. Missing general Python dependencies initially interrupted bookkeeping.
   With user authorization, PyYAML 6.0.3, NumPy 2.5.3 and Matplotlib 3.11.2
   were installed in `.venv`; analysis then completed. No physics rerun was needed.
4. The PNG was visually inspected and displays the expected Z resonance.

## Prompt-to-code mapping

| Specification | MadGraph script |
|---|---|
| SM | `import model sm` |
| pp → l+l− | `generate p p > l+ l-` |
| Electron and muon channels (analysis choice) | `define l+ = e+ mu+`, `define l- = e- mu-` |
| 14 TeV | `set ebeam1 7000`, `set ebeam2 7000` |
| 50,000 events (analysis choice) | `set nevents 50000` |
| Reproducible seed | `set iseed 12345` |
| Generation cuts (analysis choice) | `set ptl 10`, `set etal 2.5`, `set mmll 50` |
| PDF | `set pdlabel nn23lo1` |
| Parton level | No shower or detector enabled |

| Observable / normalization | Python analysis |
|---|---|
| Dilepton invariant mass | `mass2 = total[3]**2 - np.dot(total[:3], total[:3])` |
| Cross-section normalization | `per_event = sigma / n` with actual `n = len(masses)` |
| Differential distribution | `density = counts * per_event / np.diff(edges)` |
| MC statistical uncertainty | `error = np.sqrt(counts) * per_event / np.diff(edges)` |

Positive constant cross-section weights with LHE `IDWTUP=-4` were verified.
Each event represents 0.02840978 pb. Error bars show bin MC statistical
uncertainty; integration, PDF and scale uncertainties are not included.

## Artifacts and reproduction

- `scripts/mg5_dy_ll_14tev_50k_run2.mg5`: generation settings.
- `events/dy_ll_14tev_50k_run2/Events/run_01/unweighted_events.lhe.gz`: events.
- `events/dy_ll_14tev_50k_run2/Events/run_01/run_01_tag_1_banner.txt`: authoritative settings.
- `scripts/plot_mll_dy_ll_14tev_50k_run2.py`: validation and plotting.
- `output/figures/mll_dy_ll_14tev_50k_run2.png` and `.pdf`: plots.
- `output/data/mll_dy_ll_14tev_50k_run2.csv`: histogram and uncertainties.
- `output/data/mll_dy_ll_14tev_50k_run2_metadata.json`: normalization and checks.

From the repository root, regenerate the figure from the existing events with:

```bash
.venv/bin/python -m pip install numpy matplotlib
.venv/bin/python scripts/plot_mll_dy_ll_14tev_50k_run2.py
```

The generated `events/` directory is kept locally and excluded from Git. A fresh
clone includes the generation scripts, histogram data, and figures, but needs
the LHE sample and its banner before rerunning the plotting script. Generate
them using `scripts/mg5_dy_ll_14tev_50k_run2.mg5` through the Magnus MadGraph
compile and launch workflow described in `src/blueprints/README.md`.
