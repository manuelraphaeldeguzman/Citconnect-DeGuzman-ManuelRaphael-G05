# Citconnect

Citconnect is a Django-based Wi-Fi voucher management system developed for CIT-U.

## Features

- User registration, login, and logout
- Student and staff roles
- Role-based dashboards
- User profile management
- Voucher creation, updating, and deletion
- Voucher assignment to students
- Student voucher viewing
- Server-side form validation
- Access control and authentication
- Automated tests for account and voucher workflows

## Technologies Used

- Python
- Django
- PostgreSQL
- HTML, CSS, Bootstrap
- Git and GitHub

## Requirements

- Python 3.12 or later (use a version compatible with the project's dependencies)
- PostgreSQL
- Git

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/manuelraphaeldeguzman/Citconnect-DeGuzman-ManuelRaphael-G05.git
   cd Citconnect-DeGuzman-ManuelRaphael-G05
   ```

2. Create and activate a virtual environment (Windows):

   ```cmd
   py -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies:

   ```cmd
   pip install -r requirements.txt
   ```

4. Create your environment file:

   ```cmd
   copy .env.example .env
   ```

5. Edit `.env` and provide your own Django secret key and PostgreSQL database credentials.

   Do not commit your `.env` file or share its contents.

6. Apply database migrations:

   ```cmd
   py manage.py migrate
   ```

7. Start the development server:

   ```cmd
   py manage.py runserver
   ```

8. Open the application:

   http://127.0.0.1:8000/

## Running Tests

Run the complete automated test suite:

```cmd
py manage.py test
```

To reuse an existing test database during development:

```cmd
py manage.py test --keepdb
```

The test suite covers account and voucher workflows, validation, authentication, role restrictions, and student data access.

## Environment Variables

The application reads its configuration from `.env`.

| Variable | Description |
|---|---|
| SECRET_KEY | Django secret key |
| DEBUG | Enables or disables Django debug mode |
| DB_NAME | PostgreSQL database name |
| DB_USER | PostgreSQL username |
| DB_PASSWORD | PostgreSQL password |
| DB_HOST | PostgreSQL server hostname |
| DB_PORT | PostgreSQL server port |

## Security Notes

- Keep `.env` private and out of version control.
- Use `DEBUG=False` outside local development.
- Do not expose database credentials or Django secret keys.
- The local SQLite database file is excluded from version control.

## Development

The project uses Git branches and pull requests for integrating changes into the `develop` and `main` branches.
