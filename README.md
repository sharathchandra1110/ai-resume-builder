# Resume AI Builder

Resume AI Builder is a FastAPI-based project that helps you save a profile, paste a target job description, measure resume fit, and generate a job-focused resume in HTML or PDF.

The project now includes:

- A FastAPI backend for profile storage, skill analysis, resume scoring, and resume generation
- A built-in frontend served by FastAPI at `/app/`
- Two resume templates:
  - `ats_single_column`
  - `modern_two_column`
- Resume preview, HTML rendering, and PDF export

## Features

- Save structured profile data including projects, experience, certifications, and links
- Save a structured job description with `target_title` and `company_name`
- Extract and normalize technical skills from the job description
- Match profile skills against job requirements
- Generate:
  - fit analysis
  - resume score
  - summary
  - preview data
  - HTML resume
  - PDF resume
- Use the browser UI at `/app/` instead of calling the API manually

## Project Structure

```text
resume-ai-builder/
├── backend/
│   ├── main.py
│   ├── models/
│   ├── services/
│   ├── templates/
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── generated/
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10+
- `pip`

## Installation

Create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run The App

Start the FastAPI server:

```bash
venv/bin/python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Open:

- Frontend UI: `http://127.0.0.1:8000/app/`
- Swagger docs: `http://127.0.0.1:8000/docs`
- Health endpoint: `http://127.0.0.1:8000/health`

## Frontend Path

The frontend is served directly by FastAPI:

- `/app/` -> browser UI
- `/app` -> redirects to `/app/`

This frontend lets you:

- save a profile
- save a job description
- select a resume template
- preview the resume in-page
- open the rendered HTML resume
- download the PDF
- reset backend state

## Main API Flow

Typical usage order:

1. `POST /profile`
2. `POST /job-description`
3. `GET /analysis/fit`
4. `GET /resume/preview`
5. `GET /resume/html` or `GET /resume/view`
6. `GET /resume/pdf`

## Important Endpoints

### Core

- `GET /`
- `GET /health`
- `DELETE /state/reset`

### Profile

- `POST /profile`
- `GET /profile`

### Job Description

- `POST /job-description`
- `GET /job-description`
- `GET /job-description/skills`

### Analysis

- `GET /skill-match`
- `GET /resume-score`
- `GET /skill-recommendations`
- `GET /analysis/fit`

### Resume

- `GET /resume/skills`
- `GET /resume/summary`
- `GET /resume/skills-section`
- `GET /resume/preview`
- `GET /resume/full`
- `GET /resume/html`
- `GET /resume/view`
- `GET /resume/pdf`
- `GET /templates`

## Request Models

### `POST /profile`

Example payload:

```json
{
  "name": "Sharath Chandra Karupakala",
  "email": "sharath@example.com",
  "skills": [
    "Java",
    "Spring Boot",
    "REST APIs",
    "MySQL",
    "Git"
  ],
  "education": "B.Tech in Computer Science and Engineering",
  "phone": "+91 98765 43210",
  "location": "Hyderabad, India",
  "headline": "Java Backend Developer",
  "core_competencies": [
    "Backend Development",
    "API Design",
    "Problem Solving"
  ],
  "experience": [
    {
      "title": "Backend Developer Intern",
      "subtitle": "Academic Innovation Lab",
      "duration": "2024",
      "description": "Supported backend feature development and API integration.",
      "technologies": [
        "Java",
        "REST APIs",
        "Git"
      ],
      "highlights": [
        "Implemented API endpoints",
        "Fixed backend bugs"
      ],
      "link": ""
    }
  ],
  "projects": [
    {
      "title": "Inventory Management API",
      "subtitle": "Personal Project",
      "duration": "2025",
      "description": "Built secure backend APIs for inventory and orders.",
      "technologies": [
        "Java",
        "Spring Boot",
        "MySQL",
        "JWT"
      ],
      "highlights": [
        "Implemented CRUD endpoints",
        "Added JWT authentication"
      ],
      "link": "https://github.com/username/project"
    }
  ],
  "certifications": [
    "Java Fundamentals"
  ],
  "links": {
    "GitHub": "https://github.com/username",
    "LinkedIn": "https://linkedin.com/in/username"
  }
}
```

### `POST /job-description`

Example payload:

```json
{
  "jd_text": "We are hiring a Java Backend Developer with Spring Boot, REST APIs, MySQL, Docker, and Git experience.",
  "target_title": "Java Backend Developer",
  "company_name": "Example Tech"
}
```

## Templates

Available templates:

- `ats_single_column`: sample-inspired professional blue single-column resume
- `modern_two_column`: two-column resume with skills sidebar

You can choose a template with:

```text
/resume/preview?template_id=ats_single_column
/resume/html?template_id=modern_two_column
/resume/pdf?template_id=ats_single_column
```

## PDF Output

Generated PDF files are written to:

```text
generated/
```

The PDF endpoint returns the generated file directly as a download.

## State Storage

The app stores the latest profile and job description locally in:

```text
backend/data/app_state.json
```

This file is ignored by git.

## Notes

- The backend currently stores one active profile and one active job description at a time.
- `GET /resume/view` returns rendered HTML directly in the browser.
- If PDF generation fails, make sure the project dependencies are installed correctly.

## Development Notes

Useful commands:

```bash
python3 -m compileall backend
git status --short
```

## Next Improvements

- Add authentication and multi-user storage
- Save multiple resumes per user
- Add editable template themes
- Connect a database instead of local file storage
- Add export history and saved resume versions
