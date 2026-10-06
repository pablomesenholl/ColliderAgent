# MadGraph event generation

Status: STOPPED — compile failed; no launch, retry, fix, or fallback performed.

SM LO `p p > l+ l-`, with `l+ = e+ mu+`, `l- = e- mu-`.
Beam energies: 7000 GeV each. Requested events: 50000. Seed: 12345.
Generation cuts: lepton pT > 10 GeV, |eta| < 2.5, dilepton invariant mass > 50 GeV.
PDF: built-in nn23lo1. No shower or detector simulation. Systematic variations disabled.

Reproducible script: `scripts/mg5_dy_ll_14tev_50k.mg5`.
Output: `events/dy_ll_14tev_50k` (verified absent before submission).

User requires stopping immediately on any failed computational/tool step or detected bug, without fixing, retrying, or falling back.

Compile job ID: `97163027e913f90b`.
Job result: `success=false`, `Compilation failed (return code 1).`
MadGraph 3.7.0 encountered `IndexError: list index out of range` during `quit`, in its automatic update routine:

```text
madgraph/interface/madgraph_interface.py, line 7157, in install_update
    data[sline[0]] = int(sline[1])
IndexError: list index out of range
```

The compile script reached process output before failing at shutdown. The pipeline reports compilation failure, so no validated compiled artifact was downloaded and no events were generated. User's strict stop requirement took precedence over the skill's general repair/retry guidance.
