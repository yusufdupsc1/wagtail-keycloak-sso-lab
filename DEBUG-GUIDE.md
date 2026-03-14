# SSO Debug Guide — Wagtail + Keycloak

> Systematic debugging procedures for production SSO failures.

---

## Quick Diagnostic Flow

```
SSO Login → Where does it fail?

├─ BEFORE Keycloak page → Redirect URI mismatch
├─ ON Keycloak page → Credentials/Account issue  
├─ AFTER Keycloak return → Token/Callback issue
├─ AT Django session → Cookie/Session issue
└─ AT Admin access → Staff/Permission issue
```

---

## Phase 1: Gather Information

Ask client:
1. Error message exactly?
2. Before or after Keycloak login?
3. Fresh setup or was working before?
4. Recent changes (upgrades)?

---

## Phase 2: Check Keycloak

### 2.1 Valid Redirect URIs
- Must match Django callback EXACTLY
- Trailing slash matters: `/callback/` ≠ `/callback`
- Protocol: http vs https

### 2.2 Client Credentials
- Client ID matches Django
- Client secret correct (copy-paste from Keycloak)

### 2.3 Authentication Flow
- Standard Flow enabled
- Direct Access Grants disabled (for OIDC)

### 2.4 User
- User exists in Keycloak
- User enabled
- User has email

---

## Phase 3: Check Django

### 3.1 Settings
```python
SOCIALACCOUNT_PROVIDERS = {
    'keycloak': {
        'KEYCLOAK_URL': 'http://localhost:8080',
        'KEYCLOAK_REALM': 'wagtail-realm',
        'APP': {
            'client_id': 'wagtail-app',
            'secret': 'CLIENT_SECRET_HERE'
        }
    }
}
```

### 3.2 Adapter
```python
SOCIALACCOUNT_ADAPTER = 'accounts.adapters.KeycloakSocialAccountAdapter'
```

### 3.3 Cookie Settings (Django 4.x)
```python
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'
```

---

## Phase 4: Enable Debug Logging

```python
# settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'loggers': {
        'allauth': {'handlers': ['console'], 'level': 'DEBUG'},
        'django.security': {'handlers': ['console'], 'level': 'DEBUG'},
    },
}
```

---

## Phase 5: Trace OAuth2 Flow

```
1. GET /accounts/keycloak/login/
   → Redirects to Keycloak?

2. Keycloak login
   → User authenticates?

3. Callback with code
   → /callback/?code=XXX&state=YYY

4. Token exchange
   → POST /token (client_id, client_secret, code)
   → Returns access_token + id_token

5. User creation
   → Django creates/updates user

6. Session
   → Session cookie set

7. Redirect to dashboard
   → User logged in
```

---

## Common Issues & Fixes

### Issue 1: redirect_uri_mismatch
**Fix:** Copy exact URI from Django to Keycloak

### Issue 2: invalid_client  
**Fix:** Verify client secret matches exactly

### Issue 3: User not created
**Fix:** Custom adapter with `is_open_for_signup=True`

### Issue 4: User can't access admin
**Fix:** Map Keycloak role to Django is_staff

### Issue 5: Session lost
**Fix:** Check SameSite cookie settings

---

## Debug Commands

```bash
# Test Keycloak endpoints
curl http://localhost:8080/auth/realms/wagtail-realm/.well-known/openid-configuration

# Check Django users
docker compose exec django python manage.py shell
from django.contrib.auth import get_user_model
User = get_user_model()
print(User.objects.count())

# Check social accounts
from allauth.socialaccount.models import SocialAccount
print(SocialAccount.objects.count())
```

---

## Emergency Rollback

If SSO breaks production:
1. Disable SSO: `SOCIALACCOUNT_PROVIDERS = {}`
2. Ensure password login works
3. Deploy
4. Fix SSO in staging
5. Deploy fix
