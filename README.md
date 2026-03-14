# Wagtail + Keycloak SSO Lab

Working lab for debugging Keycloak SSO with Django/Wagtail.

## Quick Start

```bash
docker compose up -d --build
```

Configure Keycloak:
1. Create realm: `wagtail-realm`
2. Create client: `wagtail-app`
3. Set redirect URIs to `http://localhost:8000/accounts/keycloak/login/callback/`
4. Get client secret

Set client secret in environment, then:
```bash
docker compose exec django python manage.py migrate
docker compose exec django python manage.py createsuperuser
```

## Structure

```
django/
├── wagtail_project/     # Django + Wagtail config
├── accounts/            # Custom SSO adapter
└── templates/         # Basic templates
```

## Key Files

- `docker-compose.yml` - PostgreSQL, Keycloak, Django
- `django/accounts/adapters.py` - Custom user mapping
- `DEBUG-GUIDE.md` - Debug procedures
- `ERROR-MAPPING.md` - Common errors

## Notes

- Keycloak: http://localhost:8080
- Django: http://localhost:8000

Test SSO: http://localhost:8000/accounts/keycloak/login/
