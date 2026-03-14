# SSO Authentication Service

Production SSO integration service with Keycloak identity provider.

## Overview

OAuth2/OIDC authentication service integrated with Keycloak. Provides secure single sign-on for web applications.

## Features

- OAuth2 Authorization Code flow with PKCE
- JWT token validation
- User provisioning with role mapping
- Session management
- Staff/admin role synchronization

## Tech Stack

- Django 4.2
- django-allauth
- Keycloak
- PostgreSQL
- Docker

## Quick Start

```bash
docker compose up -d
```

## Configuration

Environment variables required. See `.env.example`.

## Endpoints

- `/admin/` — Django admin
- `/accounts/` — Authentication endpoints

## License

MIT
