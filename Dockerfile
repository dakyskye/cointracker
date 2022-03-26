FROM python:3.10.3-alpine3.15

WORKDIR /tmp
COPY Pipfile* .
RUN \
  apk add --no-cache --virtual .build-deps \
    build-base \
    gcc \
    libffi-dev \
    && \
  apk add --no-cache chromium chromium-chromedriver && \
  pip install pipenv && \
  pipenv lock --keep-outdated --requirements > requirements.txt && \
  pip install -r ./requirements.txt && \
  rm -f requirements.txt && \
  apk del --no-cache .build-deps

WORKDIR /
COPY cointracker ./cointracker/
CMD ["python", "-m", "cointracker"]