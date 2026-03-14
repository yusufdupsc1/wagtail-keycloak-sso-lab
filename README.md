# Wagtail + Keycloak SSO Debug Lab

Production debugging lab for Keycloak SSO integration with Django/Wagtail.

## Problem

Wagtail upgrade from 2.x to 7.x broke Keycloak SSO integration. This lab reproduces the issue and documents the debugging methodology.

## Stack

| Component | Version |
|-----------|---------|
| Wagtail | 7.x |
| Django | 4.2 |
| django-allauth | 65.x |
| Keycloak | 11.x |

## Architecture

```
Browser → Django → django-allauth → OIDC → Keycloak
         ← token ← code ← auth ←
```

## Auth Flow

1. User requests /admin/
2. Django redirects to Keycloak
3. User authenticates
4. Keycloak returns with authorization code
5. Django exchanges code for tokens
6. Django validates JWT via JWKS
7. User provisioned, session created
8. Access granted to Wagtail admin

## Debugging Model

All SSO issues fall into one of five buckets:

1. **Redirect URI mismatch** — Error on Keycloak
2. **Callback validation** — State/nonce invalid
3. **Token exchange** — Client secret wrong
4. **Session persistence** — Cookie/SameSite issue
5. **Authorization** — User lacks is_staff

See `sso-triage-checklist.md` for systematic diagnosis.

## Quick Start

```bash
# Start services
docker compose up -d

# Configure Keycloak
# 1. Open http://localhost:8080
# 2. Create realm: demo-realm
# 3. Create client: wagtail-demo
# 4. Set redirect URIs

# Run Django
docker compose exec django python manage.py migrate
docker compose exec django python manage.py createsuperuser

# Test SSO
# Visit http://localhost:8000/admin/
```

## Files

| File | Purpose |
|------|---------|
| docker-compose.yml | Full stack |
| architecture.md | System design |
| sso-triage-checklist.md | Debug procedures |
| failure-scenarios.md | Common breakage patterns |
| debug-report-template.md | Root cause template |

## Why This Matters

SSO failures in production = users can't work.

This lab demonstrates systematic debugging methodology for production authentication issues.

## Notes

- Keycloak: http://localhost:8080
- Django: http://localhost:8000
- Admin: http://localhost:8000/admin/
