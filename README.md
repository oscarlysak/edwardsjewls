# Edwards Jewelers Django Project

## Project Setup Instructions

This guide will walk you through setting up the Edwards Jewelers Django project with PostgreSQL using Docker. Please follow the steps below to get the project running on your local machine.

### Prerequisites

- **Docker**: Ensure Docker is installed on your machine. You can download and install it from [here](https://www.docker.com/get-started).
- **Docker Compose**: Docker Compose is typically included with Docker Desktop. Verify installation by running `docker-compose --version` in your terminal.

### Initial Setup

**Clone the Repository:**

```sh
git clone <repository_url>
cd edwardsjewelers
```

**Create and Activate Virtual Environment** (optional but recommended for local development without Docker):

```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scriptsctivate`
```

**Install Python Dependencies:**

```sh
pip install -r requirements.txt
```

### Using Docker

#### Building and Running the Containers

**Build the Docker Containers:**

```sh
docker-compose build
```

**Start the PostgreSQL Container:**

```sh
docker-compose up -d db
```

**Run Database Migrations:**

Open a new terminal window and navigate to the project directory. Run the following commands to create the necessary database tables:

```sh
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate
```

**Create a Superuser:**

Create a superuser to access the Django admin interface:

```sh
docker-compose run web python manage.py createsuperuser
```

**Start All Services:**

Start all the services, including the web application and pgAdmin:

```sh
docker-compose up -d
```

**Access the Application:**

- **Django Application**: Open your web browser and go to `http://0.0.0.0:8000`.
- **Django Admin Interface**: Go to `http://0.0.0.0:8000/admin` and log in with the superuser credentials you created.
- **pgAdmin**: Go to `http://0.0.0.0:5050` and log in with:
  - Email: `admin@admin.com`
  - Password: `root`

  Add a new server in pgAdmin with the following details:
  - Hostname: `db`
  - Username: `edwaeardsjewelersadmin`
  - Password: `edwardsjewelerspassword`

### Without Docker (Local Development)

If you prefer to run the project without Docker, follow these steps:

1. **Ensure PostgreSQL is Installed:**

   Install PostgreSQL on your local machine and create a database with the following credentials:

   - Database: `edwardsjewelersdb`
   - User: `edwaeardsjewelersadmin`
   - Password: `edwardsjewelerspassword`

2. **Update settings.py:**

   Ensure your `settings.py` is configured to connect to your local PostgreSQL instance.

3. **Run Migrations:**

   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a Superuser:**

   ```sh
   python manage.py createsuperuser
   ```

5. **Run the Development Server:**

   ```sh
   python manage.py runserver
   ```

6. **Access the Application:**

   - **Django Application**: Open your web browser and go to `http://127.0.0.1:8000`.
   - **Django Admin Interface**: Go to `http://127.0.0.1:8000/admin` and log in with the superuser credentials you created.

### Common Docker Commands

- **Stop Containers:**

  ```sh
  docker-compose down
  ```

- **View Logs:**

  ```sh
  docker-compose logs
  ```

- **Access Container Shell:**

  ```sh
  docker-compose run web sh
  ```

### Troubleshooting

- **Database Connection Issues**: Ensure the PostgreSQL container is running and the environment variables in `docker-compose.yml` match those in `settings.py`.
- **Docker Build Errors**: Ensure all dependencies are correctly listed in `requirements.txt`.

For further assistance, refer to the [Django documentation](https://docs.djangoproject.com/en/stable/) and [Docker documentation](https://docs.docker.com/).