FROM python:3.10-slim

WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY security_group_updater.py .

# Default command (can be overridden by KubernetesPodOperator)
CMD ["python", "security_group_updater.py"]