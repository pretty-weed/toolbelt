FROM ubuntu:latest
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    rsync \
    unzip \
    ca-certificates \
    nodejs\
    npm \
    git \
    && rm -rf /var/lib/apt/lists/*
