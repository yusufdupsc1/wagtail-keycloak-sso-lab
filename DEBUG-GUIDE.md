# SSO Debug Guide

## Debug Sequence

1. **Before Keycloak** - Redirect URI mismatch
2. **On Keycloak** - Credentials/user issue
3. **After callback** - Token exchange failed
4. **Session** - Cookie/SameSite issue
5. **Admin access** - Missing is_staff

## Common Issues

| Issue | Fix |
|-------|-----|
| redirect_uri_mismatch | Exact match in Keycloak |
| invalid_client | Check client secret |
| User not created | Add is_open_for_signup adapter |
| 403 on /admin | Map Keycloak role to is_staff |
| Session lost | Check SAMESITE=Lax |

## Debug Log

```python
LOGGING = {
    'version': 1,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'loggers': {
        'allauth': {'handlers': ['console'], 'level': 'DEBUG'},
    },
}
```

## Key Endpoints

- Discovery: `/auth/realms/{realm}/.well-known/openid-configuration`
- JWKS: `/auth/realms/{realm}/protocol/openid-connect/certs`
- Token: `/auth/realms/{realm}/protocol/openid-connect/token`

## Adapter

```python
class KeycloakSocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        return True
    
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        roles = data.get('realm_access', {}).get('roles', [])
        if 'admin' in roles:
            user.is_staff = True
        return user
```
