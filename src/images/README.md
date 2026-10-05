# ColliderAgent — Container Images

**Dockerfiles for the containers that Magnus blueprints run inside.**

Each subdirectory is a standalone build context. Images are pushed to
`git.pku.edu.cn/rise-agi/<name>:latest` and referenced from blueprints'
`container_image` field.

## Images

| Directory | Image | Used by |
|---|---|---|
| [`collider/`](collider/) | `collideragent/collider:mg5-3.7.0-fixed` | `madgraph-compile`, `madgraph-compile-no-update`, `madgraph-launch` |
| [`micromegas/`](micromegas/) | `rise-agi/micromegas:latest` | `micromegas-compile`, `micromegas-calc` |

### MadGraph compiler-template repair

The collider image derives from a pinned upstream image containing MadGraph 3.7.0.
Its generated `Template/LO/Source/make_opts` contains only NUL bytes, while the
original `.make_opts` template is intact. The derived image removes the damaged
cache so MadGraph regenerates it on startup, preserving the installed toolchain.

Build on the Docker host used by local Magnus before running the MadGraph blueprints:

```bash
docker build -t collideragent/collider:mg5-3.7.0-fixed src/images/collider
```

Local Magnus uses this cached image without a registry upload. For other workers,
publish the built image to a registry they can access and update the three MadGraph
blueprints' `container_image` references to the published digest.

Verified with a 100-event SM `p p > e+ e-` test at 14 TeV (seed 12345):
baseline Magnus job `7f8b4f9edbab9f96` failed during compilation; repaired-image
job `4ee8105770dab87b` generated all 100 LHE events with both MG5 exit codes zero.

### What's baked in

The micrOmegas image includes `magnus-sdk>=0.8.0` so that its blueprint entry commands can
invoke `magnus` CLI and `import magnus` immediately, without paying a
10–30 s `pip install` cost per job. Bump the version in the Dockerfile and
rebuild when the station SDK advances.

| Image | Extra bundled tooling |
|---|---|
| `micromegas:latest` | `micromegas 6.3.0` with its CalcHEP symbolic engine **pre-compiled**, plus `gcc/g++/gfortran`, `libgsl`, `liblapack`, `libX11` (CalcHEP hard dep) |

## Build & Push

Each image is self-contained (downloads its dependencies at build time from
upstream sources such as Zenodo / apt). To publish:

```bash
cd src/images/<name>
docker build -t git.pku.edu.cn/rise-agi/<name>:latest .
docker login git.pku.edu.cn           # requires deploy token with write to rise-agi/*
docker push git.pku.edu.cn/rise-agi/<name>:latest
```

## Licensing

All bundled software is redistributable under its original license:

| Package | License | Notes |
|---|---|---|
| micrOmegas 6.3.0 | CC-BY-4.0 | DOI-backed Zenodo distribution, arXiv:2312.14894 |

The Dockerfiles fetch upstream tarballs directly; we do not vendor any
proprietary binaries. Images that depend on licensed software (e.g. Mathematica)
are expected to mount the license at runtime rather than bake it in —
see the existing `mma-het` image for that pattern.
