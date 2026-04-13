# Project Internship Portal

A project-centric internship portal built with a FastAPI backend, a static HTML/CSS/JavaScript frontend, and SQLite for storage.

## Overview

This project connects two kinds of users:

- `student`: creates a profile, adds projects, discovers recommended internships, and applies using selected projects
- `company`: creates a profile, posts internships, views recommended student projects, and manages applications

The platform is centered around the idea that projects can demonstrate capability better than a resume alone.

## Screenshots

![Internship Portal screenshot 1](Photos/Screenshot%202026-04-13%20143635.png)

![Internship Portal screenshot 2](Photos/Screenshot%202026-04-13%20143742.png)

![Internship Portal screenshot 3](Photos/Screenshot%202026-04-13%20143827.png)

![Internship Portal screenshot 4](Photos/Screenshot%202026-04-13%20143852.png)

![Internship Portal screenshot 5](Photos/Screenshot%202026-04-13%20144029.png)

![Internship Portal screenshot 6](Photos/Screenshot%202026-04-13%20144039.png)

## Tech Stack

- Backend: FastAPI, SQLAlchemy, Pydantic
- Auth: JWT-based authentication
- Database: SQLite
- Frontend: static HTML, CSS, JavaScript
- Recommendation engine: TF-IDF + cosine similarity using scikit-learn

## Repository Structure

```text
backend/app/
  core/          auth, security, shared dependencies
  database/      SQLAlchemy base and session
  models/        database models
  routers/       API routes
  schemas/       request/response schemas
  services/      recommendation logic
  utils/         text cleaning and similarity helpers

frontend/
  assets/css/    global styles
  assets/js/     page scripts and API calls
  pages/         auth, student, and company pages

data/
  app.db         SQLite database
```

## Main Features

- User registration and login
- Role-based access for students and companies
- Student profile management
- Company profile management
- Student project creation and listing
- Internship posting and listing
- Internship recommendations for students
- Project recommendations for companies
- Internship applications with 1 to 3 linked projects
- Application status updates for companies

## Backend API Areas

- `/auth` for registration and login
- `/student` for student profile and student project actions
- `/company` for company profile and internship actions
- `/applications` plus role-specific application views

## Local Setup

### 1. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install backend dependencies

```powershell
pip install -r backend/app/requirements.txt
```

### 3. Run the backend

From the repository root:

```powershell
uvicorn backend.app.main:app --reload
```

The backend will start on `http://localhost:8000`.

### 4. Open the frontend

Open [frontend/index.html](frontend/index.html) in the browser, or serve the `frontend/` directory with a simple local static server.

## Current Notes

- The database is a local SQLite file at `data/app.db`
- Tables are created automatically on backend startup
- The project is currently in MVP/prototype form
- The frontend expects the backend at `http://localhost:8000`

## Known Improvement Areas

- move secrets and environment-specific config out of source code
- tighten database constraints and validation
- align a few frontend/backend API contracts
- replace startup table creation with migrations
- improve documentation and test coverage
