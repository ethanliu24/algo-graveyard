# Build front end
FROM node:20-alpine3.19 AS frontend

WORKDIR /frontend

COPY package.json package-lock.json vite.config.mjs vite.prod.config.mjs README.md /frontend/
COPY ./js /frontend/js
COPY ./styles /frontend/styles
COPY ./static /frontend/static

RUN npm ci
RUN npm run build


# Build backend
FROM python:3.13 AS backend

# Install dependencies for Weasyprint
RUN apt-get update && apt-get install -y \
    build-essential \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    fonts-liberation \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies for PlayWright
RUN apt-get update && apt-get install -y \
    wget gnupg2 curl unzip \
    libnss3 libatk-bridge2.0-0 libx11-xcb1 libxcomposite1 libxcursor1 \
    libxdamage1 libxi6 libxtst6 libcups2 libxrandr2 libgbm1 libasound2 \
    libpangocairo-1.0-0 libpango-1.0-0 fonts-liberation libappindicator3-1 \
    lsb-release xdg-utils --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /algograveyard

COPY ./requirements.txt /algograveyard/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /algograveyard/requirements.txt
RUN playwright install chromium

COPY . .
COPY --from=frontend /frontend/static /algograveyard//static

ENV APP_ENV=production

EXPOSE 80

CMD ["fastapi", "run", "app/main.py", "--port", "80"]