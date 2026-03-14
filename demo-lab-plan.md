# Demo Lab Implementation Plan

## Environment Setup

### Prerequisites
- Docker
- Docker Compose
- 4GB RAM
- Ports: 5432, 8080, 8000

### Boot Order

```bash
# 1. Start PostgreSQL
docker compose up -d postgres

# 2. Wait for PostgreSQL (10s)
sleep 10

# 3. Start Django (run migrations)
docker compose up -d django
docker compose exec django python manage.py migrate

# 4. Start Keycloak
docker compose up -d keycloak
```

## Keycloak Realm Import

### Option 1: Manual

1. Open http://localhost:8080
2. Login: admin / admin
3. Create realm: demo-realm
4. Create client: wagtail-demo

### Option 2: Realm Export

```bash
docker cp realm-export.json keycloak:/tmp/
docker exec keycloak /opt/keycloak/bin/kc.sh import --file=/tmp/realm-export.json
```

## Django Bootstrap

```bash
# Run migrations
docker compose exec django python manage.py migrate

# Create superuser
docker compose exec django python manage.py createsuperuser

# Collect static
docker compose exec django python manage.py collectstatic --noinput
```

## OIDC Configuration

### Django Settings

```python
SOCIALACCOUNT_PROVIDERS = {
    'keycloak': {
        'KEYCLOAK_URL': 'http://localhost:8080',
        'KEYCLOAK_REALM': 'demo-realm',
        'APP': {
            'client_id': 'wagtail-demo',
            'secret': 'CLIENT_SECRET_HERE'
        }
    }
}
```

### Keycloak Client Settings

| Setting | Value |
|---------|-------|
| Client ID | wagtail-demo |
| Access Type | confidential |
| Valid Redirect URIs | http://localhost:8000/accounts/oidc/keycloak/login/callback/ |
| Web Origins | http://localhost:8000 |
| Authentication Flow | Standard |

## Login Verification

### Test Flow

1. Visit: http://localhost:8000/admin/
2. Redirected to Keycloak
3. Login: yusuf@example.com
4. Redirect back to Django
5. Access granted to /admin/

### Success Criteria

- [ ] Redirect to Keycloak works
- [ ] Login form displays
- [ ] Callback returns with code
- [ ] Token exchange succeeds
- [ ] User created in Django
- [ ] Session cookie set
- [ ] Admin access granted

## Failure Injection Experiments

### Test 1: Redirect URI Mismatch

1. Change Keycloak redirect URI
2. Attempt login
3. Observe: redirect_uri_mismatch error

### Test 2: Wrong Client Secret

1. Set incorrect client secret in Django
2. Attempt login
3. Observe: invalid_client error

### Test 3: SameSite Issue

1. Remove SESSION_COOKIE_SAMESITE
2. Attempt login
3. Observe: session not persisting

### Test 4: Missing is_staff

1. Remove role mapping in adapter
2. Login as admin user
3. Observe: 403 on /admin/
