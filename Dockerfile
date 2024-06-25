# Stage 1: Build stage
FROM python:3.12-slim AS build
WORKDIR /src
COPY requirements.txt ./
RUN python -m venv venv \
    && . venv/bin/activate \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

# Stage 2: Production stage
FROM python:3.12-slim

WORKDIR /src

COPY --from=build /src/venv /src/venv/
COPY . .
ENV PATH="/src/venv/bin:$PATH"

RUN useradd -m speaker-user
USER speaker-user

CMD [ "python","app/app.py" ]