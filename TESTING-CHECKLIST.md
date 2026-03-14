# Testing Checklist

## 1. Start Services
```bash
docker compose up -d --build
```

## 2. Configure Keycloak

1. Open http://localhost:8080
2. Login: admin / admin
3. Create realm: `wagtail-realm`
4. Create client: `wagtail-app`
   - Access Type: confidential
   - Valid Redirect URIs:
     ```
     http://localhost:8000/accounts/keycloak/login/callback/
     ```
   - Web Origins: `http://localhost:8000`
5. Get client secret from Credentials tab
6. Create user: testadmin / testpass123

## 3. Configure Django

Set client secret in environment, then:
```bash
docker compose exec django python manage.py migrate
docker compose exec django python manage.py createsuperuser
```

## 4. Test

Visit: http://localhost:8000/accounts/keycloak/login/

## Issues

- redirect_uri_mismatch → Check Keycloak redirect URIs
- invalid_client → Check client secret
- 403 on /admin → Check is_staff mapping
