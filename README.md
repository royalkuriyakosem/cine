# filmhub: Film Production Management Platform

## 1. Overview

**filmhub** is a comprehensive, containerized film production management platform designed to streamline the entire filmmaking process from pre-production to post-production. It is built with a robust **Django** backend serving a RESTful API and a modern **React** frontend powered by Vite. The entire development environment is orchestrated with **Docker Compose**, ensuring consistency and ease of setup.

## 2. Technology Stack

-   **Backend:**
    -   **Framework:** Django (Python 3.11)
    -   **API:** Django REST Framework
    -   **Authentication:** JWT (djangorestframework-simplejwt)
    -   **Database:** PostgreSQL
    -   **Asynchronous Tasks:** Celery with Redis as the message broker
    -   **WSGI Server:** Gunicorn
    -   **Libraries:** `django-filter` for filtering, `reportlab` for PDF generation.
-   **Frontend:**
    -   **Framework:** React
    -   **Build Tool:** Vite
    -   **Runtime:** Node.js
-   **DevOps:**
    -   **Containerization:** Docker & Docker Compose

## 3. Core Features & Implemented Modules

The backend is organized into modular Django apps, each responsible for a specific domain of film production.

### a. Accounts & Permissions (`accounts` app)

This app manages user identity, roles, and access control.

-   **Custom User Model:** Extends Django's `AbstractUser` with a `role` field, defining specific roles within a production (e.g., `ADMIN`, `PRODUCER`, `DIRECTOR`, `CREW`).
-   **JWT Authentication:** Secure, token-based authentication with endpoints for obtaining, refreshing, and verifying JWTs.
-   **Role-Based Permissions:** A custom permission system (`role_required`) restricts access to certain API endpoints based on the user's assigned role.
-   **Data Seeding:** Includes a management command (`create_default_roles`) to automatically create a user for each predefined role, simplifying testing and setup.

### b. Production Management (`productions` app)

This is the central app for managing core production data.

-   **Data Models:** `Production`, `Scene`, `Shot`, and `BudgetLine` to track everything from high-level project details to granular shot information.
-   **RESTful API:** Provides full CRUD (Create, Read, Update, Delete) functionality for all models.
-   **Filtering & Search:** Endpoints support powerful filtering (e.g., by production status) and text-based search.
-   **Automatic Ownership:** When a new production is created via the API, its `owner` is automatically set to the authenticated user.

### c. Scheduling & Reporting (`scheduling` app)

This app handles the day-to-day operational logistics of a film shoot.

-   **Data Models:** `CallSheet`, `DailyProductionReport (DPR)`, and `CrewCheckIn`.
-   **Specialized API Endpoints:**
    -   **Call Sheet Management:** Endpoints for creating, updating, and publishing call sheets, restricted to users with appropriate roles (e.g., `UPM_AD`).
    -   **Crew Check-in:** A dedicated endpoint (`/check-in/`) allows assigned crew members to log their arrival on set.
    -   **Personalized Call Sheets:** An endpoint (`/my-call-sheets/`) allows a logged-in crew member to view only the published call sheets they are assigned to.
-   **PDF Generation:** A dynamic endpoint (`/pdf/`) generates a simple, printable PDF version of any call sheet.

### d. Placeholder Apps

The project is scaffolded with additional apps (`vfx`, `media`, `finance`) that are ready for future implementation.

## 4. Frontend

The frontend is a standard **React** application set up with **Vite** for a fast development experience. It is fully containerized and configured to connect to the backend API, ready for UI development.

## 5. Development Environment & Setup

The entire application stack is defined in the `docker-compose.yml` file, enabling a one-command setup.

### Prerequisites
- Docker
- Docker Compose

### Installation & Launch
1.  Clone the repository.
2.  From the project root directory, build and start all services:
    ```sh
    docker-compose up --build -d
    ```
3.  Create a superuser account to access the admin panel:
    ```sh
    docker-compose exec web python manage.py createsuperuser
    ```
    Follow the prompts to set a username, email, and password.
4.  (Optional) Seed the database with default users for each role:
    ```sh
    docker-compose exec web python manage.py create_default_roles
    ```

### Access URLs
-   **Frontend:** `http://localhost:3000`
-   **Backend API:** `http://localhost:8000`
-   **Django Admin:** `http://localhost:8000/admin/`
