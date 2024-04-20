# FastAPI Backend Wobot Assignment

## Technology Stack and Features

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com) for the Python backend API.
    - 🧰 [SQLAlchemy](https://sqlalchemy.org/) for the Python SQL database interactions (ORM).
    - 🔍 [Pydantic](https://docs.pydantic.dev), used by FastAPI, for the data validation and settings management.
    - 💾 [MySQL](https://www.mysql.com/) as the SQL database.
- 🐋 [Docker Compose](https://www.docker.com) for development and production.
- 🔒 Secure password hashing by default.
- 🔑 JWT token authentication.

## Requirements

* [Docker](https://www.docker.com/).


## How To Use It

You can **just fork or clone** this repository and use it as is.


### Configure

```bash
doker-compose up --build
```

**Note**: The first time you start your stack, it might take a minute for it to be ready. While the backend waits for the database to be ready and configures everything. You can check the logs to monitor it.

* The project includes automatic database migrations.

* Now you can open your browser and interact with:

Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://127.0.0.1:8000/docs

### Note
- The .env file contains some basic secrets for easy configuration. You can update/change if you want to.
