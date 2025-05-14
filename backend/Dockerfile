###########
# BUILDER #
###########

FROM python:3.12.2-alpine AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY ./app/requirements.txt .

RUN apk add --no-cache \
    gcc \
    musl-dev \
    mariadb-connector-c-dev \
    pkgconfig

RUN pip install --upgrade pip
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

#######
# APP #
#######

FROM python:3.12.2-alpine AS equipment_backend

WORKDIR /home/app/web

RUN apk add --no-cache \
    mariadb-connector-c \
    libstdc++

COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

COPY ./entrypoint.sh ./entrypoint.sh
COPY ./app ./app

RUN addgroup -S app && \
    adduser -S -G app -h /home/app/web app && \
    chown -R app:app /home/app/web && \
    chmod -R u+w /home/app/web

USER app

ENV PYTHONPATH=/home/app/web/app

RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]