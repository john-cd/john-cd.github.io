# Dockerfile build inputs are required and supplied by Compose from tracked .devcontainer/.env.
# From the repo root pass --env-file .devcontainer/.env and add --env-file .devcontainer/.env.local when present.
# Small Ubuntu-based Dev Container with a checksum-verified Zola binary and site tools.
FROM ubuntu:24.04

# Compose supplies these public release pins from .devcontainer/.env.
ARG ZOLA_VERSION
ARG ZOLA_SHA256

LABEL org.opencontainers.image.source="https://github.com/john-cd/john-cd.github.io"

# Install only the tools needed to work on the site, then remove package indexes and archives.
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install --yes --no-install-recommends \
        ca-certificates \
        curl \
        git \
        python3 \
        sudo \
    && groupadd --gid 1000 vscode \
    && useradd --uid 1000 --gid vscode --create-home --shell /bin/bash vscode \
    && printf '%s ALL=(ALL) NOPASSWD:ALL\n' vscode > /etc/sudoers.d/vscode \
    && chmod 0440 /etc/sudoers.d/vscode \
    && curl --fail --silent --show-error --location --retry 3 \
        "https://github.com/getzola/zola/releases/download/v${ZOLA_VERSION}/zola-v${ZOLA_VERSION}-x86_64-unknown-linux-gnu.tar.gz" \
        --output /tmp/zola.tar.gz \
    && echo "${ZOLA_SHA256}  /tmp/zola.tar.gz" | sha256sum --check --status \
    && tar -xzf /tmp/zola.tar.gz -C /usr/local/bin zola \
    && chmod 0755 /usr/local/bin/zola \
    && rm /tmp/zola.tar.gz \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Run the preview and editor tools as a regular development user.
USER vscode
