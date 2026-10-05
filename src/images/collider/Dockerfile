FROM git.pku.edu.cn/het-agi/collider@sha256:1bf6d8db2cb9348f965c3c6650f1c6af8234c1d8be0b49040ddd55e79a33c1a5

# The base image has a zero-filled generated make_opts file. MadGraph recreates
# this cache from its intact, version-matched .make_opts template on startup.
RUN rm /opt/MG5_aMC_v3_7_0/Template/LO/Source/make_opts
