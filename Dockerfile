# Multi-stage build for minimal final image
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ src/
COPY pyproject.toml .
COPY README.md .
COPY LICENSE .

# Install the package
RUN pip install .

# Final stage - minimal runtime image
FROM python:3.11-slim

# Install git (required for the tool to work)
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy installed package from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/smart-commits-ai /usr/local/bin/smart-commits-ai

# Create working directory
WORKDIR /workspace

# Set entrypoint
ENTRYPOINT ["smart-commits-ai"]
CMD ["--help"]
