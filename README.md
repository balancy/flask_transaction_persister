# Web app for transaction processing

## Description

This project is a processing system designed to handle transaction data in real-time. It consists of an API for collecting transaction data, asynchronous processing with message queuing, and persisting in a database. The system supports distributed tracing and performance monitoring.

## Components

1. **Flask-based Web App**: Provides a REST API for collecting transaction data.
2. **Celery and RabbitMQ**: Used for asynchronous processing of transactions.
3. **PostgreSQL**: Database for storing incoming and processed transactions.
4. **Jaeger**: Enables distributed tracing of requests across the system.
5. **Prometheus + Grafana**: Used for performance metrics and visualization.
6. **Pytest**: Ensures testing coverage and reliability of the codebase.
7. **Locust**: Conducts load testing to validate system performance under traffic.
8. **Poetry**: Manages project dependencies and environment setup.
9. **Ruff + Black**: Provides linting and code formatting to ensure code quality and adherence to style guidelines.
10. **Docker Compose**: Simplifies the process of running the entire application stack.

The web app follows a layered architecture with a dependency injection mechanism to promote modularity and testability.

## Workflow

**Flask app**
1. Receives a POST request containing transaction data.
2. Validates the data using Pydantic schemas.
3. Saves the incoming transaction to the PostgreSQL database.
4. Sends the transaction to a RabbitMQ queue for further processing.

**Celery app**
1. Consumes the transaction from the RabbitMQ queue.
2. Validates the data using Pydantic schemas.
3. Fetches the exchange rate from an external API.
4. Converts the transaction amount to EUR and saves the processed transaction in the database.

## Installation for local development

Ensure you have Git and Docker Compose installed on your machine.

1. Clone the repository

```sh
git clone https://github.com/balancy/flask_transaction_persister.git
```

2. Run the app in development mode

```sh
make
```

3. Run tests
```sh
make test
```

4. Access monitoring and tracing:
- Jager (Tracing): http://localhost:16686
- Grafana (Metrics): http://localhost:3000


5. Run load testing

```sh
make load
```

Load testing interface: http://localhost:8089

Note: The system is designed to handle at least 1000 transactions per minute, validated through load testing with Locust.

## Installation for production

Ensure you have Git and Docker Compose installed on your remote machine.

1. Clone the repository

```sh
git clone https://github.com/balancy/flask_transaction_persister.git
```

2. Run the app in production mode

```sh
make prod
```