FROM nvidia/cuda:12.2.2-devel-ubuntu22.04

ENV PYTHONUNBUFFERED TRUE

RUN chmod 1777 /tmp 
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
    fakeroot \
    ca-certificates \
    g++ \
    git \
    python3-dev \
    openjdk-8-jdk-headless \
    curl \
    libgtk2.0-dev \
    && rm -rf /var/lib/apt/lists/* \
    && cd /tmp \
    && curl -O https://bootstrap.pypa.io/get-pip.py \
    && python3 get-pip.py
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1
RUN update-alternatives --install /usr/local/bin/pip pip /usr/local/bin/pip3 1

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install -e .
RUN pip install -e ".[train]"
RUN pip install flash-attn --no-build-isolation

ENV PYTHONPATH=/app:$PYTHONPATH