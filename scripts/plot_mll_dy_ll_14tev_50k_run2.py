#!/usr/bin/env python3
"""Validate and histogram the generated LO dilepton LHE sample (no regeneration)."""
import argparse
import csv
import gzip
import hashlib
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--lhe', type=Path, default=Path('events/dy_ll_14tev_50k_run2/Events/run_01/unweighted_events.lhe.gz'))
    ap.add_argument('--banner', type=Path, default=Path('events/dy_ll_14tev_50k_run2/Events/run_01/run_01_tag_1_banner.txt'))
    ap.add_argument('--output', type=Path, default=Path('output'))
    args = ap.parse_args()
    banner = args.banner.read_text()
    expected = {'nevents': '50000', 'ebeam1': '7000.0', 'ebeam2': '7000.0', 'pdlabel': 'nn23lo1', 'ptl': '10.0', 'etal': '2.5', 'mmll': '50.0'}
    for key, val in expected.items():
        match = re.search(r'^\s*(\S+)\s*=\s*' + key + r'\s*[!#]', banner, re.M)
        assert match and match[1] == val, f'Unexpected banner setting {key}'
    for command in ['import model sm', 'define l+ = e+ mu+', 'define l- = e- mu-', 'generate p p > l+ l-']:
        assert command in banner, f'Missing process command {command}'
    masses, weights, flavors = [], [], []
    init = None
    with gzip.open(args.lhe, 'rt') as stream:
        for _, element in ET.iterparse(stream, events=('end',)):
            if element.tag == 'init':
                lines = element.text.strip().splitlines()
                header = lines[0].split()
                assert header[:2] == ['2212', '2212'] and list(map(float, header[2:4])) == [7000., 7000.]
                assert int(header[8]) == -4, 'Unexpected event weight convention'
                processes = [list(map(float, line.split())) for line in lines[1:1+int(header[9])]]
                init = (sum(row[0] for row in processes), sum(row[1]**2 for row in processes)**0.5)
            elif element.tag == 'event':
                lines = element.text.strip().splitlines()
                head = lines[0].split()
                rows = [row.split() for row in lines[1:1+int(head[0])]]
                final = [row for row in rows if int(row[1]) == 1]
                assert len(final) == 2, 'Unexpected final-state multiplicity'
                ids = [int(row[0]) for row in final]
                assert ids[0] == -ids[1] and abs(ids[0]) in (11, 13), 'Invalid dilepton flavor or charge'
                vectors = np.array([[float(x) for x in row[6:10]] for row in final])
                assert np.isfinite(vectors).all() and (vectors[:, 3] > 0).all(), 'Invalid momenta'
                assert np.allclose(vectors[:, 3]**2, np.sum(vectors[:, :3]**2, axis=1), rtol=1e-7, atol=1e-5), 'Invalid mass-shell condition'
                incoming = np.array([[float(x) for x in row[6:10]] for row in rows if int(row[1]) == -1])
                assert np.allclose(incoming.sum(axis=0), vectors.sum(axis=0), rtol=1e-8, atol=1e-5), 'Four-momentum nonconservation'
                pt = np.hypot(vectors[:, 0], vectors[:, 1])
                eta = np.arcsinh(vectors[:, 2] / pt)
                total = vectors.sum(axis=0)
                mass2 = total[3]**2 - np.dot(total[:3], total[:3])
                assert mass2 >= 0, 'Negative invariant mass squared'
                mass = np.sqrt(mass2)
                assert (pt >= 10-1e-6).all() and (np.abs(eta) <= 2.5+1e-6).all() and mass >= 50-1e-6, 'Generation cut violated'
                masses.append(mass)
                weights.append(float(head[2]))
                flavors.append(abs(ids[0]))
                element.clear()
    masses, weights, flavors = map(np.array, (masses, weights, flavors))
    n = len(masses)
    assert n == 50000 and init is not None, f'Unexpected actual event count: {n}'
    sigma, sigma_error = init
    assert (weights > 0).all() and np.allclose(weights, sigma, rtol=1e-7), 'IDWTUP=-4 weights not constant cross-section weights'
    # For this positive, unweighted IDWTUP=-4 sample each event represents sigma/N.
    per_event = sigma / n
    edges = np.arange(50., 202., 2.)
    counts, _ = np.histogram(masses, edges)
    density = counts * per_event / np.diff(edges)
    error = np.sqrt(counts) * per_event / np.diff(edges)
    centers = (edges[:-1] + edges[1:])/2
    figures, data = args.output/'figures', args.output/'data'
    figures.mkdir(parents=True, exist_ok=True)
    data.mkdir(parents=True, exist_ok=True)
    stem = 'mll_dy_ll_14tev_50k_run2'
    with (data/f'{stem}.csv').open('w', newline='') as stream:
        writer = csv.writer(stream, lineterminator='\n')
        writer.writerow(['mll_low_GeV', 'mll_high_GeV', 'events', 'dsigma_dm_pb_per_GeV', 'mc_stat_error_pb_per_GeV'])
        writer.writerows(zip(edges[:-1], edges[1:], counts, density, error))
    metadata = dict(events=n, electron_events=int((flavors == 11).sum()), muon_events=int((flavors == 13).sum()), cross_section_pb=sigma, integration_error_pb=sigma_error, idwtup=-4, event_weight_pb=per_event, normalization='sigma/N_actual; positive constant LHE cross-section weights verified', uncertainty='sqrt(bin_count)*sigma/N/bin_width; integration uncertainty not included', mass_min_GeV=float(masses.min()), mass_max_GeV=float(masses.max()), underflow=int((masses < 50).sum()), overflow_above_200=int((masses > 200).sum()), visible_events=int(counts.sum()), settings=expected, lhe=str(args.lhe), banner=str(args.banner), lhe_sha256=hashlib.sha256(args.lhe.read_bytes()).hexdigest())
    (data/f'{stem}_metadata.json').write_text(json.dumps(metadata, indent=2)+'\n')
    fig, ax = plt.subplots(figsize=(8.2, 5.6), layout='constrained')
    ax.stairs(density, edges, color='#1464a0', linewidth=1.8, label=r'$e^+e^- + \mu^+\mu^-$')
    ax.errorbar(centers, density, yerr=error, fmt='none', ecolor='#1464a0', elinewidth=.8, capsize=1.4, label='MC statistical uncertainty')
    ax.set(xlim=(50,200), yscale='log', xlabel=r'$m_{\ell\ell}$ [GeV]', ylabel=r'$d\sigma/dm_{\ell\ell}$ [pb/GeV]', title=r'SM Drell–Yan at the 14 TeV LHC')
    ax.text(.98, .96, 'Parton level · LO · NNPDF2.3 LO\n50,000 unweighted events · 2 GeV bins\n'+r'$p_T^\ell > 10$ GeV, $|\eta_\ell| < 2.5$, $m_{\ell\ell} > 50$ GeV', transform=ax.transAxes, ha='right', va='top', fontsize=9)
    ax.grid(True, which='major', alpha=.2)
    ax.legend(loc='lower left', frameon=False, fontsize=9)
    for suffix in ['png', 'pdf']:
        fig.savefig(figures/f'{stem}.{suffix}', dpi=180)
    plt.close(fig)
    print(json.dumps(metadata, indent=2))


if __name__ == '__main__':
    main()
