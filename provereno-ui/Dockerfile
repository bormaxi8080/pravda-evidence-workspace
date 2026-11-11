# linux/arm64 MAC-DEV baseline; native amd64 qualification is separate.
FROM python:3.12.10-slim-bookworm@sha256:fd95fa221297a88e1cf49c55ec1828edd7c5a428187e67b5d1805692d11588db AS base
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_DISABLE_PIP_VERSION_CHECK=1
# Immutable Debian archive fixes the native dependency resolution universe.
RUN rm /etc/apt/sources.list.d/debian.sources && printf '%s\n' \
    'deb [check-valid-until=no] https://snapshot.debian.org/archive/debian/20251101T000000Z bookworm main' \
    'deb [check-valid-until=no] https://snapshot.debian.org/archive/debian-security/20251101T000000Z bookworm-security main' \
    > /etc/apt/sources.list

FROM base AS wheel
WORKDIR /build
COPY locks/build.txt /locks/build.txt
RUN pip install --no-cache-dir --require-hashes -r /locks/build.txt
COPY pyproject.toml ./
COPY provereno ./provereno
ENV SOURCE_DATE_EPOCH=1746057600
RUN pip wheel --no-deps --no-build-isolation --wheel-dir /wheel . && sha256sum /wheel/*.whl > /wheel/wheel.sha256

FROM base AS dependency-base
COPY locks /locks
COPY --from=wheel /wheel /wheel
RUN python -m venv --without-pip /opt/venv

FROM dependency-base AS web-dependencies
RUN pip --python /opt/venv install --no-cache-dir --only-binary=:all: --require-hashes -r /locks/web.txt && \
    pip --python /opt/venv install --no-deps --no-cache-dir /wheel/*.whl && \
    pip --python /opt/venv check

FROM dependency-base AS capture-dependencies
RUN pip --python /opt/venv install --no-cache-dir --only-binary=:all: --require-hashes -r /locks/capture.txt && \
    pip --python /opt/venv install --no-deps --no-cache-dir /wheel/*.whl && \
    pip --python /opt/venv check

FROM dependency-base AS offline-dependencies
RUN pip --python /opt/venv install --no-cache-dir --only-binary=:all: --require-hashes -r /locks/offline.txt && \
    pip --python /opt/venv install --no-deps --no-cache-dir /wheel/*.whl && \
    pip --python /opt/venv check

FROM base AS runtime
ENV PATH=/opt/venv/bin:$PATH HOME=/tmp
RUN groupadd --gid 10001 provereno && useradd --uid 10001 --gid 10001 --no-create-home --home-dir /tmp provereno && \
    rm -rf /usr/local/lib/python3.12/site-packages/pip* /usr/local/bin/pip* /root/.cache
WORKDIR /runtime
COPY --from=wheel /wheel/wheel.sha256 /usr/share/provereno/wheel.sha256
# No implicit data volume, runtime configuration, secrets, or source-tree overlay.

FROM runtime AS web
COPY --from=web-dependencies /opt/venv /opt/venv
USER 10001:10001
CMD ["uvicorn", "provereno.main:app", "--host", "0.0.0.0", "--port", "8080"]

FROM runtime AS capture
ENV PLAYWRIGHT_BROWSERS_PATH=/opt/browsers
COPY --from=capture-dependencies /opt/venv /opt/venv
RUN apt-get update && apt-get install -y --no-install-recommends \
    libnss3 libnspr4 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
    libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2 \
    libpango-1.0-0 libcairo2 libx11-6 libxcb1 libxext6 libxshmfence1 fonts-liberation \
    fonts-noto-color-emoji && rm -rf /var/lib/apt/lists/* && \
    python -m playwright install chromium && chmod -R a+rX /opt/browsers
USER 10001:10001
# Inventory only: no job admission or unqualified public capture.
CMD ["python", "-m", "provereno.image_info", "capture"]

FROM runtime AS offline
COPY --from=offline-dependencies /opt/venv /opt/venv
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0 fonts-liberation && \
    rm -rf /var/lib/apt/lists/*
USER 10001:10001
CMD ["python", "-m", "provereno.image_info", "offline"]

# An unqualified default build must also select the browser-free web role.
FROM web AS default
