FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    XDG_CACHE_HOME=/tmp/resume-cache \
    PATH=/opt/resume-venv/bin:$PATH

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates nodejs npm python3 python3-venv \
        libreoffice-writer poppler-utils fontconfig \
        fonts-crosextra-carlito fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/resume-builder
COPY requirements.txt ./
RUN python3 -m venv /opt/resume-venv \
    && python -m pip install --no-cache-dir -r requirements.txt

COPY vendor/claude-resume-generator ./vendor/claude-resume-generator
RUN npm ci --omit=dev --prefix vendor/claude-resume-generator \
    && npm cache clean --force
COPY scripts/build_verified_resume.py ./scripts/build_verified_resume.py
RUN python scripts/build_verified_resume.py --self-test

WORKDIR /work
ENTRYPOINT ["/opt/resume-venv/bin/python", "/opt/resume-builder/scripts/build_verified_resume.py"]
