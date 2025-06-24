# MindCare 
Distributed systems project 

**MindCare** is a microservices-based emotional diary and mood analysis application designed to help users track, understand, and reflect on their emotional state over time.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Tech Stack](#tech-stack)
4. [Folder Structure](#folder-structure)
5. [Getting Started](#getting-started)

   * [Prerequisites](#prerequisites)
   * [Installation & Run](#installation--run)
6. [API Endpoints](#api-endpoints)
7. [Frontend Features](#frontend-features)
8. [Future Enhancements](#future-enhancements)
9. [License](#license)

---

## Project Overview

MindCare provides a simple, intuitive interface for users to record daily emotional journal entries. It employs backend microservices to store, analyze, and generate personalized advice based on detected emotions, helping users gain insights and support for their emotional well‑being.

---

## Architecture

MindCare follows a microservices architecture, with each service containerized via Docker and communicating over REST APIs:

* **Auth Service (port 8000)**: Manages user registration and authentication concerns (login planned for future release).
* **Diary Service (port 8001)**: Handles create/read operations for journal entries, backed by SQLite.
* **Analysis Service (port 8002)**: Processes text entries to detect dominant emotion (e.g., joy, sadness, anger).
* **Advice Service (port 8003)**: Delivers personalized advice based on identified emotion.
* **Frontend**: Static HTML/CSS/JS interface interacting asynchronously with the services.

All services are orchestrated using Docker Compose for easy startup and scaling.

---

## Tech Stack

**Backend:**

* Python 3.10+
* FastAPI (REST framework with auto-generated OpenAPI)
* SQLAlchemy (ORM for SQLite in Diary Service)
* Pydantic (data validation)
* aiohttp & asyncio (asynchronous inter-service HTTP calls)
* Docker & Docker Compose

**Frontend:**

* HTML, CSS, JavaScript
* Chart.js (visualization of emotional trends)

---

## Folder Structure

```
mindcare/
├── auth_service/          # Authentication microservice
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── diary_service/         # Emotional diary microservice
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── analysis_service/      # Text analysis microservice
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── advice_service/        # Advice microservice
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── frontend/              # Static HTML/CSS/JS UI
│   └── index.html
└── docker-compose.yml     # Compose file for all services
```

---

## Getting Started

### Prerequisites

* Docker & Docker Compose installed
* Python 3.10+ (for frontend HTTP server, optional)

### Installation & Run

1. Clone the repository:

   ```bash
   git clone https://github.com/pavlicL/mindcare.git
   cd mindcare
   ```
2. Build and start all services:

   ```bash
   docker-compose up --build
   ```
3. In a new terminal, serve the frontend:

   ```bash
   cd frontend
   python3 -m http.server 5500
   ```
4. Open your browser at `http://localhost:5500/index.html` to use MindCare.

---

## API Endpoints

### Auth Service (8000)

* `POST /register` – Register a new user

### Diary Service (8001)

* `POST /entry` – Add a single journal entry
* `POST /bulk-entry` – Add multiple entries at once
* `GET /entries/{username}` – Retrieve all entries for a user

### Analysis Service (8002)

* `POST /analyze-text` – Analyze text payload and return detected emotion

### Advice Service (8003)

* `GET /advice/{emotion}` – Get personalized advice for a given emotion

---

## Frontend Features

* **Asynchronous API calls** using Fetch API
* **Entry dashboard**: Table view of past entries
* **Emotional trend charts** powered by Chart.js
* **Dynamic advice** display after each entry submission

---

## Future Enhancements

* User login with JWT authentication
* Notification Service for entry reminders
* Move from SQLite to a scalable database (e.g., DynamoDB)
* Extend Auth Service with full login/logout flows

---

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

