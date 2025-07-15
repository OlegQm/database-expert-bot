FROM python:3.10.14-slim-bookworm
WORKDIR /webapp
COPY . .
ARG OPENAI_API_KEY="default"
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "-m", "streamlit", "run", "app_and_bot/application.py"]
