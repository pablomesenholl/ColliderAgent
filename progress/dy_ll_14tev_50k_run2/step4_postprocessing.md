# Step 4: dilepton invariant mass distribution

Completed from the existing parton-level LHE sample; no regeneration and no shower or detector simulation.

Run `.venv/bin/python scripts/plot_mll_dy_ll_14tev_50k_run2.py` from the repository root.

Inputs:
- `events/dy_ll_14tev_50k_run2/Events/run_01/unweighted_events.lhe.gz`
- `events/dy_ll_14tev_50k_run2/Events/run_01/run_01_tag_1_banner.txt`

Verified SM process `p p > l+ l-`, with e/mu flavors, 7 TeV proton beams, nn23lo1 PDF, and generation cuts pT > 10 GeV, |eta| < 2.5, mll > 50 GeV. All 50,000 events contain exactly two opposite-sign, same-flavor final-state e/mu leptons. Finite momenta, mass-shell conditions, four-momentum conservation, and generation cuts pass for every event. Electron channel: 24,840; muon channel: 25,160.

LHE IDWTUP = -4 and positive constant cross-section weights verified. Total cross section is 1420.489 pb with integration error 1.331787 pb. Each event represents sigma/N_actual = 0.02840978 pb. Histogram normalization uses actual generated count, not requested count. Error bars are sqrt(N_bin)*sigma/N_actual/bin_width; generator integration error and scale/PDF uncertainties are not included.

Mass range in sample: 50.006–780.230 GeV. Main plot covers 50–200 GeV in 2 GeV bins with logarithmic y axis. The visible range contains 49,918 events; 82 events are above 200 GeV; no underflow. Visually inspected the final PNG: axes, units, legend, cuts and expected Z resonance near 91 GeV are clear.

Outputs:
- `output/figures/mll_dy_ll_14tev_50k_run2.png`
- `output/figures/mll_dy_ll_14tev_50k_run2.pdf`
- `output/data/mll_dy_ll_14tev_50k_run2.csv`
- `output/data/mll_dy_ll_14tev_50k_run2_metadata.json`

NumPy 2.5.3 and Matplotlib 3.11.2 installed into the existing virtual environment under the user's authorization for generic dependency resolution. Matplotlib automatically used a temporary cache directory because its default user configuration directory is read-only in this environment; plotting completed successfully. No ColliderAgent or Magnus-specific issue encountered during this step.
