# Project Management Assistant

This project automates the process of gathering product feedback from X (formerly Twitter), analyzing its sentiment, and creating actionable tasks in Trello. It integrates Google Cloud Scheduler, the X API, Google Gemini API, and the Trello API to streamline this workflow for product teams.

## Overview

The core function is to monitor X for mentions or comments about a product, use AI to understand the sentiment, and then push relevant feedback directly into the product team's Trello workflow.

## How it Works

1.  **Scheduled Trigger:** Google Cloud Scheduler periodically triggers the processing pipeline.
2.  **Fetch Feedback:** The pipeline connects to the X API using the provided bearer token to fetch recent comments or mentions related to the product based on configured search criteria.
3.  **Sentiment Analysis:** The fetched comments are processed by the Google Gemini API (using the provided API key) to analyze their sentiment (e.g., positive, negative, neutral, feature request, bug report).
4.  **Trello Task Creation:** Comments identified as requiring review by the product team (based on the sentiment analysis) are automatically added as new cards to a designated Trello board and list.

## Features

* **X (Twitter) Monitoring:** Fetches product feedback directly from X.
* **AI-Powered Sentiment Analysis:** Leverages Google Gemini to understand user feedback.
* **Automated Trello Task Creation:** Creates Trello cards for actionable feedback items.
* **Scheduled Workflow Execution:** Uses Google Cloud Scheduler for regular, automated runs.
* **Asynchronous Processing:** Employs Celery & Redis for efficient background task handling.
* **Stateless Design:** Built for scalability and reliability.
* **Dockerized Deployment:** Simplified setup using Docker Compose.

## Technology Stack

* Python
* Google Cloud Scheduler
* Google Gemini API
* X API (Twitter API v2)
* Trello API
* Celery
* Redis
* Docker

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/abdulmunimjemal/product-mgmt-assistant
    cd product-mgmt-assistant
    ```
2.  **Configure Environment Variables:**
    * Create a `.env` file in the project's root directory.
    * Add the following required variables:
        ```dotenv
        GEMINI_API_KEY=YOUR_GEMINI_API_KEY
        X_BEARER_TOKEN=YOUR_X_API_BEARER_TOKEN
        # Details for Trello API (Key, Token, Board/List IDs) is included at the launch of the pipeline
        ```
3.  **Build and Run with Docker:**
    ```bash
    docker-compose up --build
    ```
4.  **Service Running:**
    * The backend service (if applicable for direct interaction or triggering) will be running on `http://localhost:8000`.
    * You can modify the port mapping in the `docker-compose.yml` file if needed. The core workflow runs based on the Google Cloud Scheduler trigger.

## Usage

1.  **Configure:** Ensure all necessary environment variables in the `.env` file are correctly set, including X search terms, Trello board/list IDs, and API keys/tokens.
2.  **Deploy:** Run the application using `docker-compose up --build`.
3.  **Schedule:** Set up a job in Google Cloud Scheduler to periodically send a request (e.g., HTTP POST) to the appropriate trigger endpoint exposed by this service (endpoint details need to be defined within the application).
4.  **Monitor:** Check the designated Trello board for new cards generated from X feedback as the scheduled job runs.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue to discuss proposed changes or enhancements.

---
© 2025
