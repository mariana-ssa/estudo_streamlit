FROM python:3.10-slim

WORKDIR /app

RUN apt update -y \
    && apt upgrade -y

COPY requirements.txt .
COPY main.py .

RUN pip install \
    --upgrade pip \
    --no-cache-dir \
    uv \
    && uv pip install --system -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "main.py"]
CMD ["--server.address=0.0.0.0", "--server.port=8501"]
