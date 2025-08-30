# AI News Aggregator

This project is a FastAPI-based AI News Aggregator that uses the OpenAI API to generate news summaries from various sources.

## Local Development

These instructions will guide you through setting up and running the application locally for development and testing purposes.

All commands should be run from the root of the project.

### Prerequisites

*   Docker Desktop installed and running.
*   An OpenAI API key.

### 1. Configuration

1.  **Create an environment file:**
    Copy the example environment file in the `backend` directory to a new `.env` file.
    ```bash
    cp backend/.env.example backend/.env
    ```

2.  **Set your API Key:**
    Open the `backend/.env` file and add your OpenAI API key:
    ```
    OPENAI_API_KEY=YOUR_OPENAI_API_KEY
    ```

### 2. Running the Application

To build and run the application, execute the following command:

```bash
docker compose -f backend/docker-compose.yml up --build -d backend
```

This will start the FastAPI application, and it will be accessible at `http://localhost:8000`.

### 3. Running Tests

To run the test suite, execute this command:

```bash
docker compose -f backend/docker-compose.yml run --rm test
```

**Note:** This command only runs the tests and does not start the web server. It will build the image if it doesn't exist, run `pytest`, and then remove the container automatically.

### 4. Testing the API

Once the **application is running** (using the command from step 2), you can send a test request to the `/generate-news` endpoint using `curl`:

```bash
curl -X POST -H "Content-Type: application/json" -d '{}' http://localhost:8000/api/v1/generate-news
```

### 5. Viewing Logs

To view the logs of the running application container, use the following command:

```bash
docker logs -f backend-backend-1
```

### 6. Stopping the Application

To stop and remove the application containers and network, run the following command:

```bash
docker compose -f backend/docker-compose.yml down
```
