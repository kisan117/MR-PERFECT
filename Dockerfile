# Python base image
FROM python:3.8-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
    wget \
    curl \
    gnupg \
    ca-certificates \
    unzip \
    libgdk-pixbuf2.0-0 \
    libpangocairo-1.0-0 \
    libgtk-3-0 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libgbm1 \
    libasound2 \
    libpango1.0-0 \
    libvulkan1 \  # Vulkan dependency add kiya
    xdg-utils && \  # xdg-utils dependency add kiya
    # Google Chrome install karo
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable_current_amd64.deb && \
    apt-get -f install -y && \
    # ChromeDriver install karo
    LATEST=$(wget -q -O - https://chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget https://chromedriver.storage.googleapis.com/$LATEST/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/ && \
    rm chromedriver_linux64.zip && \
    # Python dependencies install karo
    pip install --no-cache-dir -r requirements.txt

# Working directory set karo
WORKDIR /app

# Application port expose karo
EXPOSE 5000

# Application start karo
CMD ["python", "main.py"]
