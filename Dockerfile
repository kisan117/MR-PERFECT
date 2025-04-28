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
    libvulkan1 \  # Vulkan dependency
    xdg-utils && \  # xdg-utils dependency
    # Install Google Chrome
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable_current_amd64.deb && \
    apt-get -f install -y && \
    # Install ChromeDriver
    LATEST=$(wget -q -O - https://chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget https://chromedriver.storage.googleapis.com/$LATEST/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/ && \
    rm chromedriver_linux64.zip && \
    # Install Python dependencies
    pip install --no-cache-dir -r requirements.txt

# Set the working directory
WORKDIR /app

# Expose the application port
EXPOSE 5000

# Start the application
CMD ["python", "main.py"]
