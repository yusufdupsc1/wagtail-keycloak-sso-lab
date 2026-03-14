# Testing Checklist

## 1. Start Django

```bash
cd django
python3 manage.py runserver 127.0.0.1:8001
```

- Django: http://127.0.0.1:8001
- Admin: http://127.0.0.1:8001/admin/
- Superuser: admin / password123

## 2. Start Keycloak (Docker)

```bash
docker run -p 8080:8080 \
  -e KEYCLOAK_ADMIN=admin \
  -e KEYCLOAK_ADMIN_PASSWORD=admin \
  quay.io/keycloak/keycloak:24.0 start-dev
```

- Keycloak: http://localhost:8080

## 3. Configure Keycloak

1. Login: admin / admin
2. Create realm: wagtail-realm
3. Create client: wagtail-app
   - Access Type: confidential
   - Redirect: http://127.0.0.1:8001/accounts/keycloak/login/callback/
4. Get client secret

## 4. Configure Django

Set in environment:
```
KEYCLOAK_CLIENT_SECRET=your-secret
```

## 5. Test SSO

Visit: http://127.0.0.1:8001/accounts/keycloak/login/

## Issues

- redirect_uri_mismatch → Check Keycloak redirect URIs
- invalid_client → Check client secret
