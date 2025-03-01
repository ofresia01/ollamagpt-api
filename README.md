# Ollama FastAPI Server

This project is a FastAPI server that integrates with Ollama's Python API to provide a chat endpoint. The server supports streaming responses, allowing real-time interaction with the language model. It can also use Prometheus to gather some simple runtime/performance metrics.

## Requirements

- Python 3.10+
- `pip` (Python package installer)
- Ollama

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/ofresia01/ollamagpt-api.git
    cd ollamagpt-api
    ```

2. Install the Ollama CLI:
    Follow the instructions on the [Ollama website](https://ollama.com) to install Ollama

3. Create and activate a virtual environment, and install the dependencies:
    * Windows:
        * ```sh
          python -m venv venv
          source venv/Scripts/activate
          pip install -r requirements.txt
          ```
    * Mac/Linux
      * ```sh
        python -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        ```

## Running the Server

To start the server, run the following command with optional arguments for the model name and whether to start Prometheus:
```sh
scripts/start.sh <model-name> <start-prometheus>
```
- `<model-name>`: The name of the model to use (default: `deepseek-r1:1.5b`).
- `<start-prometheus>`: Set to `true` to start Prometheus, `false` otherwise (default: `true`).

This script sets the PYTHONPATH and starts the FastAPI server using Uvicorn. If no model name is provided, it defaults to `deepseek-r1:1.5b`.

## Endpoints
### Root Endpoint
* **URL:** `/`
* **Method:** `GET`
* **Description:** Health check endpoint to verify that the server is running.
* **Response:** 
    ```json
    {
        "message": "Ollama FastAPI server is running!"
    }
    ```

### Chat Endpoint
* **URL:** `/chat`
* **Method:** `POST`
* **Description:** Endpoint to interact with Ollama's language model. It returns a streaming response with the model's output.
* **Request Headers:**
    - `bypass_validation` (optional): If set to `true`, input validation will be bypassed.
* **Request Body:**
    ```json
    {
        "prompt": "Your input prompt here"
    }
    ```
* **Response:** Streaming response with the model's output in plain text.

## Prometheus Metrics

The server exposes Prometheus metrics at the `/metrics` endpoint. These metrics include:
- `ollama_requests_total`: Total number of requests to Ollama.
- `ollama_errors_total`: Total number of errors from Ollama.
- `ollama_response_time`: Response time of Ollama requests.

## Running Tests

To run the Pytest unit tests, use the following command:
```sh
pytest
```
This will execute the tests defined in the `tests` directory.

To run some example Curl requests against the actively-running server, use the following command:
```sh
scripts/test_endpoints.sh
```