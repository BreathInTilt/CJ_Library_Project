


# CJ Library Project

A simple Flask-based library management system. Supports user authentication, book and member management, file import, and loan tracking. No database is used; data is handled through local CSV/text files.

## Features

- User & admin registration and login
- Add, edit, delete books
- Loan and return tracking
- Import/export data from CSV
- Basic charts and statistics

## Getting Started (Docker)

### Prerequisites
- Docker
- Docker Compose

### Run

```bash
git clone https://github.com/BreathInTilt/CJ_Library_Project.git
cd CJ_Library_Project
docker-compose up --build
````
### Or
```bash
git clone https://github.com/BreathInTilt/CJ_Library_Project.git
cd CJ_Library_Project
docker compose up --build
```

Then open: `http://127.0.0.1:5000`

### Stop

```bash
docker-compose down
```

## Project Structure

```
CJ_Library_Project/
├── app.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── templates/
├── static/
├── models/
├── utils/
```

## All located data in `/data` folder
