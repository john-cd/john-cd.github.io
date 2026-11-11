FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

ARG ZOLA_VERSION=0.19.2
ARG ZOLA_SHA256=0798e69b86c628ddcb264ebd86c8cc8dce7670b9049060bf94faa73f6857cd9c

LABEL org.opencontainers.image.source="https://github.com/john-cd/john-cd.github.io"

RUN apt-get update \
    && apt-get install --no-install-recommends -y ca-certificates curl python3 \
    && rm -rf /var/lib/apt/lists/* \
    && curl --fail --location --retry 3 \
        "https://github.com/getzola/zola/releases/download/v${ZOLA_VERSION}/zola-v${ZOLA_VERSION}-x86_64-unknown-linux-gnu.tar.gz" \
        --output /tmp/zola.tar.gz \
    && echo "${ZOLA_SHA256}  /tmp/zola.tar.gz" | sha256sum --check --status \
    && tar -xzf /tmp/zola.tar.gz -C /usr/local/bin zola \
    && chmod 0755 /usr/local/bin/zola \
    && rm /tmp/zola.tar.gz
