FROM python:3.13.0-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    lsb-release \
    wget \
    unzip \
    xvfb \
    && rm -rf /var/lib/apt/lists/*


RUN CHROME_VERSION="131.0.6778.70" \
    && echo "Chrome version: $CHROME_VERSION" \
    && CHROMEDRIVER_VERSION="131.0.6778.69" \
    && echo "ChromeDriver version: $CHROMEDRIVER_VERSION" \
    && wget -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.69/linux64/chromedriver-linux64.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip


WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=app.py

EXPOSE 5000

CMD ["flask", "run", "--debug"]
