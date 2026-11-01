FROM ubuntu:latest
ENV DEBIAN_FRONTEND=noninteractive

# Set up NVM directory and target Node version
ENV NVM_DIR=/root/.nvm
ENV NODE_VERSION=26.13.0

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    rsync \
    unzip \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN wget https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64 -O /usr/local/bin/yq
RUN chmod +x /usr/local/bin/yq
# add new packages/dev-specific packages here \/
# libatomic1 is needed for some node stuff
RUN apt-get update && apt-get install -y --no-install-recommends \
    jq \
    git \
    libatomic1 \
    && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/bash", "-c"]
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.8/install.sh | bash
RUN . "$NVM_DIR/nvm.sh" && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default
ENV PATH="$NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH"

# Verify installations
RUN node -v
RUN npm -v
