# Wagtail + Keycloak SSO Lab

> Minimal working lab to demonstrate SSO integration between Wagtail and Keycloak.

## Purpose

Proves capability to:
- Set up Keycloak as Identity Provider
- Configure Django + Wagtail with SSO
- Debug OAuth2/OIDC flow issues

## Quick Start

```bash
# 1. Start services
docker compose up -d

# 2. Configure Keycloak manually:
#    - Open http://localhost:8080
#    - Login: admin / admin
#    - Create realm: wagtail-realm
#    - Create client: wagtail-app
#    - Set redirect URIs:
#      http://localhost:8000/accounts/keycloak/login/callback/
#    - Get client secret

# 3. Set client secret
#    Edit django/.env or docker-compose.yml

# 4. Run migrations (in container)
docker compose exec django python manage.py migrate

# 5. Create superuser
docker compose exec django python manage.py createsuperuser

# 6. Test SSO
#    Visit http://localhost:8000/accounts/keycloak/login/
```

## Project Structure

```
wagtail-keycloak-sso-lab/
├── docker-compose.yml
├── django/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── wagtail_project/
│   │   ├── settings.py    # SSO config here
│   │   └── urls.py
│   └── accounts/
│       └── adapters.py    # Custom user mapping
└── README.md
```

## Key Files

| File | Purpose |
|------|---------|
| `settings.py` | SOCIALACCOUNT_PROVIDERS config |
| `adapters.py` | User + staff role mapping |
| `docker-compose.yml` | All services |

## Debug Common Issues

| Issue | Fix |
|-------|-----|
| redirect_uri mismatch | Match exactly in Keycloak |
| User not staff | Check adapters.py role mapping |
| Token error | Verify client secret |

---

Built to prove SSO debugging capability.
