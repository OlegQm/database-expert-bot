FROM python:3.10.14-slim-bookworm

WORKDIR /mcp
ENV PYTHONPATH=/mcp

COPY server_mcp/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server_mcp/ /mcp/
CMD ["python", "server.py"]
