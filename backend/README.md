# Eventify Backend Setup

This document provides instructions for setting up the backend environment for the Eventify project.

## Project Structure

The backend is organized as follows:

```
backend/
├── authentication/     # Custom user authentication app
├── core/               # Django project configurations (settings.py) 
├── docs/               # Documentation
├── events/             # Event management
├── feedback/           # User feedback system
├── media/              # Media files storage
├── notification/       # Notification system
├── payments/           # Payment processing
├── rsvp/               # RSVP functionality
├── tickets/            # Ticket management
├── utils/              # Utility functions
├── venv/               # Virtual environment
├── .env                # Environment variables
├── .gitignore          # Git ignore file
├── manage.py           # Django management script
├── README.md           # This file
└── requirements.txt    # Project dependencies
```

## Prerequisites

* Python
* MySQL
* Redis server (for Celery)
* Git

## Setting Up the Environment

### 1. Clone the Repository

```bash
git clone https://github.com/romanhumagain/Eventify.git
cd Eventify
git checkout backend
cd backend
```

### 2. Create and Activate Virtual Environment

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root directory with the following content:

# Add other environment variables as needed
```

### 5. Database Setup

#### MySQL Setup

##### Windows (using WAMP/XAMPP)

1. Install WAMP (https://www.wampserver.com/) or XAMPP (https://www.apachefriends.org/)
2. Start the MySQL service
3. Create a database named `eventify_db`

##### macOS

1. Install MySQL using Homebrew:
   ```bash
   brew install mysql
   brew services start mysql
   ```
2. Create a database:
   ```bash
   mysql -u root -p
   CREATE DATABASE eventify_db;
   ```

##### Linux (Ubuntu/Debian)

1. Install MySQL:
   ```bash
   sudo apt update
   sudo apt install mysql-server
   sudo systemctl start mysql
   ```
2. Create a database:
   ```bash
   sudo mysql
   CREATE DATABASE eventify_db;
   ```

***Note*** - ``` First setup mysql database ```

### 6. Run Migrations

Since the project uses a custom user model, you need to run migrations for the authentication app first:

```bash
python manage.py makemigrations authentication
python manage.py migrate authentication
```

Then migrate the rest of the applications:

```bash
python manage.py makemigrations authentication events feedback notification payments rsvp tickets
python manage.py migrate
```

### 7. Redis and Celery Setup

#### Install Redis

##### Windows
Download and install Redis for Windows from https://github.com/microsoftarchive/redis/releases or use WSL (Windows Subsystem for Linux).

##### macOS
```bash
brew install redis
brew services start redis
```

##### Linux
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis
```

###  Start Redis server (for Celery)

```bash
redis-server
```

###  Run Celery worker (in a separate terminal)

```bash
celery -A core worker --loglevel=info
```

```bash
celery -A core beat --loglevel=info
```

### 8. Create a Superuser (Admin)

```bash
python manage.py createsuperuser
```

### 9. Run the Development Server

```bash
python manage.py runserver
```

The server will start at http://localhost:8000/

## API Documentation

API documentation can be found at `/docs/`


### Database Connection Issues

- Ensure MySQL service is running
- Verify database credentials in the `.env` file
- Check database connectivity:



