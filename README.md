
# Web Chat Application

This application allows you to easily start a conversation with a GPT bot on your local machine using the latest technology.

## Installation

### Prerequisites

Ensure you have Python and pip installed on your machine.

### Install the Required Modules

To install the necessary dependencies, run the following command:

```bash
pip install -r requirements.txt
```

### Running the Application

Navigate to the project directory and start the application with the following command:

```bash
python -m streamlit run app_and_bot/application.py
```

After running the command, your application will be accessible at: [http://localhost:8501/](http://localhost:8501/)

## Docker

You can also run the application using Docker. Two methods are provided:

### 1. Docker Build

Build the Docker image using one of the following commands:

#### 1.1 Build with your OpenAI API key:

```bash
docker build -t app_and_bot --build-arg OPENAI_API_KEY=your_api_key .
```

#### 1.2 Build without specifying the API key (Note: This is a test feature and will be removed in future versions due to security concerns):

```bash
docker build -t app_and_bot .
```

### 2. Docker Run

After building the image, run the Docker container using the following command:

```bash
docker run -p 8501:8501 app_and_bot
```

Once the container is running, your application will be accessible at: [http://localhost:8501/](http://localhost:8501/)

### Docker Compose

You can also use Docker Compose to build and run the application. Note that the current setup uses a built-in OpenAI key, which will be removed in future versions due to security concerns. To use your own key, configure the environment variable `OPENAI_API_KEY` with your value.

```bash
docker compose build --no-cache
docker compose up
```

After running these commands, your application will be accessible at: [http://localhost:8501/](http://localhost:8501/)

## Kubernetes

To deploy the application to a Kubernetes cluster, ensure `kubectl` is installed, then run the following command in `kubernetes` directory in this project:

```bash
kubectl apply -f deployment.yaml
```

This will deploy the application to your Kubernetes cluster.
