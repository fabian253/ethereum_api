# For more information, please refer to https://aka.ms/vscode-docker-python
# platform needed for server deployment
FROM --platform=linux/amd64 python:3.9
EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
RUN python -m pip install --upgrade pip
COPY  requirements.txt .
RUN python -m pip install -r requirements.txt
# needed because of resoltion error of protobuf
RUN python -m pip install mysql-connector-python==8.0.33

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "app.main:app"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
