# Local Setup — Django + Wagtail + Keycloak

## Prerequisites

```bash
# Install Python 3.11+
python3 --version

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Install Docker
sudo apt install docker.io docker-compose
```

## Step 1: PostgreSQL

```bash
# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database
sudo -u postgres createdb wagtail_db
sudo -u postgres createuser wagtail_user
sudo -u postgres psql -c "ALTER USER wagtail_user WITH PASSWORD 'wagtail_pass';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE wagtail_db TO wagtail_user;"
```

## Step 2: Python Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install django>=4.2 wagtail>=5.0 psycopg2-binary django-allauth python-keycloak
```

## Step 3: Django Project

```bash
# Create project
django-admin startproject wagtail_project
cd wagtail_project

# Configure settings.py (see repository)

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

## Step 4: Keycloak

```bash
# Option 1: Docker (recommended)
docker run -p 8080:8080 \
  -e KEYCLOAK_ADMIN=admin \
  -e KEYCLOAK_ADMIN_PASSWORD=admin \
  quay.io/keycloak/keycloak:24.0 start-dev

# Option 2: Manual download
# Download from https://github.com/keycloak/keycloak/releases
```

## Step 5: Configure Keycloak

1. Open http://localhost:8080
2. Login: admin / admin
3. Create realm: wagtail-realm
4. Create client: wagtail-app
5. Set redirect URIs
6. Get client secret

## Step 6: Test SSO

Visit: http://localhost:8000/accounts/keycloak/login/
