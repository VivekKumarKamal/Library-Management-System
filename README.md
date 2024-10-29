# Library Management System

This project is a comprehensive Library Management System with a Flask backend and a Vue.js frontend.

### The librarian credentials are:

email: librarian@gmail.com
password: librarian

## Running the Backend

Navigate to the backend directory:
```
cd backend
```

Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

Install required packages:
```
pip install -r requirements.txt
```

Run the Flask development server:
```
flask run
```

The backend server will start running on `http://localhost:5000`.

## Running Celery

First, start the Redis server:
```
redis-server
```

In a new terminal, start the Celery worker:
```
celery -A backend.python_files.celery_config:celery worker --loglevel=info
```

In another terminal, start the Celery beat:
```
celery -A backend.python_files.celery_config:celery beat --loglevel=info
```

## Running the Frontend

Navigate to the frontend directory:
```
cd frontend/frontend
```

Install required npm packages:
```
npm install
```

Run the development server:
```
npm run serve
```

The frontend will be accessible at `http://localhost:8080`.

## Usage

Open a web browser and go to `http://localhost:8080` to access the application.