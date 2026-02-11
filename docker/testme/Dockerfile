ARG BASE_VERSION=latest
ARG BASE_REPO=ubuntu
ARG DEV_WORKDIR="/root/src/safe_copy"
ARG WORKING_COPY_DIR="/tmp/working_copy"

FROM ${BASE_REPO}:${BASE_VERSION} AS base

ARG DEV_WORKDIR
ARG WORKING_COPY_DIR

ENV WORKDIR=${DEV_WORKDIR}
ENV WORKING_COPY_DIR=${WORKING_COPY_DIR}
ENV BUILD_CONF_SUBDIR=docker/testme/
ENV BUILD_SCRIPTS_SUBDIR="${BUILD_CONF_SUBDIR}/build_scripts"
ENV BUILD_SCRIPTS_DIR="${WORKING_COPY_DIR}/${BUILD_SCRIPTS_SUBDIR}"

# =============================================================================
#  Install Packages
# =============================================================================
FROM base AS setup

ARG DEV_WORKDIR

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  apt update && apt install -y rsync iputils-ping curl git

RUN curl -fsSL https://pyenv.run | bash
# ToDo just create a bashrc file and merge with the dest
RUN echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
RUN echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
RUN echo 'eval "$(pyenv init - bash)"' >> ~/.bashrc

RUN env >> env.txt

RUN --mount=type=cache,target=/root/.cache/pip \
    python3 -m pip install toml

RUN python3 -c 'import json, pathlib, toml;workdir=pathlib.Path("${DEV_WORKDIR}");pyproject=toml.loads(workdir.joinpath("/pyproject.toml")));print(json.dumps(pyproject.get("tool", {}).get("test_container", {}).get("pythons"))) or [])' > pythons.json

# =============================================================================
#  Pre-load repo state
# =============================================================================
FROM base AS preload

RUN mkdir -p "${DEV_WORKDIR}"
WORKDIR ${DEV_WORKDIR}
RUN --mount=type=bind,target=${WORKING_COPY_DIR} \
  cp -r ${WORKING_COPY_DIR} ${DEV_WORKDIR}

# =============================================================================
#  Create dev container
# =============================================================================

FROM setup AS dev_container

COPY --from=preload ${DEV_WORKDIR} ${DEV_WORKDIR}
ARG ENTRYPOINT="/root/entrypoint.sh"
ENV BUILD_SCRIPTS_DIR="${WORKDIR}/${BUILD_SCRIPTS_SUBDIR}"
COPY --chmod=755 ${BUILD_CONF_SUBDIR}/build_scripts/entrypoint.sh ${ENTRYPOINT}
ENTRYPOINT [ "/root/entrypoint.sh" ]
