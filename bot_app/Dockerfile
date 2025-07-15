FROM python:3.10.14-slim-bookworm

WORKDIR /webapp
ENV PYTHONPATH=/webapp
ARG OPENAI_API_KEY="default"
ENV OPENAI_API_KEY=${OPENAI_API_KEY}

COPY bot_app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot_app/ /webapp/
CMD ["streamlit", "run", "app_files/application.py", "--server.port=8501", "--server.address=0.0.0.0"]
