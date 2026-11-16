FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

ARG APM_VERSION=0.35.1

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl gh make python3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://aka.ms/apm-unix -o /tmp/install-apm.sh \
    && APM_INSTALL_DIR=/usr/local/bin \
       APM_LIB_DIR=/usr/local/lib/apm \
       APM_NO_MODIFY_PATH=1 \
       sh /tmp/install-apm.sh "@v${APM_VERSION}" \
     && chmod -R a+rX /usr/local/lib/apm \
    && rm /tmp/install-apm.sh \
    && apm --version