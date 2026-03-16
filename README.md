# eventizer-backend
A City based event management system where all the events happening in a place can be managed by a single application.

## Installation

### Requirements
Docker installed on your system. 
Gemini api key (RAG Only works with this.)
paypal client secret & client ID (Payment Integration)

### Env setup
create a .env file at the root of the project.
### Environment Configuration
To set up the project, create a `.env` file and populate it with the following:

**Note: The .env should be in the root of the project.**

```bash
# Django & API Keys
DJANGO_SECRET=<django-secret>
GEMINI_API_KEY=<google-api-key>
PAYPAL_CLIENT_ID=<paypal-client-id>
PAYPAL_CLIENT_SECRET=<paypal-client-secret>
PAYPAL_BASE_URL=<paypal-url>

# MySQL Configuration
MYSQL_ROOT_PASSWORD=<root-password>
MYSQL_DATABASE_NAME=<db-name>
MYSQL_USERNAME=<sql-username>
MYSQL_PASSWORD=<sql-password>
MYSQL_HOST=db
MYSQL_PORT=<sql-port>

# Vector Database (ChromaDB)
CHROMADB_HOST=vectordb
CHROMDB_PORT=8000
CHROMADB_COLLECTION_NAME=<your_chroma_collection_name>

# Celery & Redis
CELERY_BROKER_URL=redis://redis:6379/0
```

### Run the program

**Build the docker compose**
```bash
docker compose build
```

**Run the containers**
```bash
docker compose up
```

The API's are available at **127.0.0.1:8000**. View the main app urls to view the end points.

<i>Happy coding!!!</i><br>
<i>Author: **Vishnu Prasad J S**</i>


