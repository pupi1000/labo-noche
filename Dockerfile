FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir uv && uv sync --no-dev
EXPOSE 8501
CMD ["uv", "run", "streamlit", "run", "ui/app.py", "--server.address=0.0.0.0"]
