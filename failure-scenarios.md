# Failure Scenarios

> Simulate real-world SSO breakage for debugging practice.

---

## Scenario 1: Redirect URI Mismatch

### Break
```yaml
# Keycloak - wrong redirect URI
Valid Redirect URIs:
  http://localhost:9000/accounts/oidc/keycloak/login/callback/
```

### Symptom
```
Error: redirect_uri_mismatch
```

### Diagnosis
1. Check error message - if on Keycloak page = redirect issue
2. Compare Keycloak redirect URIs with Django callback
3. Look for:
   - Trailing slash difference
   - Protocol mismatch (http/https)
   - Domain/port difference

### Fix
```yaml
# Keycloak - correct
Valid Redirect URIs:
  http://localhost:8000/accounts/oidc/keycloak/login/callback/
```

---

## Scenario 2: Wrong Client Secret

### Break
```python
# Django - wrong secret
KEYCLOAK_CLIENT_SECRET = 'wrong-secret'
```

### Symptom
```
Error: invalid_client
```

### Diagnosis
1. Check Django logs for token exchange failure
2. Verify client secret matches Keycloak exactly
3. Check client authentication method

### Fix
```python
# Django - correct secret
KEYCLOAK_CLIENT_SECRET = 'correct-secret-from-keycloak'
```

---

## Scenario 3: SameSite Cookie Issue

### Break
```python
# Django - missing SameSite
SESSION_COOKIE_SAMESITE = None  # removed
```

### Symptom
- User logs in
- Redirected to dashboard
- Immediately logged out
- Session not persisting

### Diagnosis
1. Check browser cookies
2. Verify SESSION_COOKIE_SAMESITE set
3. Check SESSION_COOKIE_SECURE for production

### Fix
```python
SESSION_COOKIE_SAMESITE = 'Lax'
```

---

## Scenario 4: Wrong Issuer

### Break
```python
# Keycloak - different realm
KEYCLOAK_REALM = 'wrong-realm'
```

### Symptom
```
Error: Token validation failed
iss claim does not match
```

### Diagnosis
1. Check Django logs
2. Verify KEYCLOAK_REALM matches Keycloak
3. Check JWKS endpoint accessible

### Fix
```python
KEYCLOAK_REALM = 'demo-realm'
```

---

## Scenario 5: Missing is_staff

### Break
```python
# Adapter - no role mapping
def populate_user(self, request, sociallogin, data):
    user = super().populate_user(request, sociallogin, data)
    # No is_staff mapping
    return user
```

### Symptom
- Login succeeds
- User created
- But 403 on /admin/

### Diagnosis
1. Check if user.is_staff = True
2. Verify adapter maps Keycloak roles
3. Check Keycloak has admin role assigned

### Fix
```python
def populate_user(self, request, sociallogin, data):
    user = super().populate_user(request, sociallogin, data)
    roles = data.get('realm_access', {}).get('roles', [])
    if 'admin' in roles:
        user.is_staff = True
        user.is_superuser = True
    return user
```

---

## Scenario 6: Expired Authorization Code

### Break
- User initiates login
- Waits 5+ minutes
- Completes login

### Symptom
```
Error: invalid_grant
Code not valid
```

### Diagnosis
1. Check code age
2. Codes expire in ~60 seconds
3. User took too long

### Fix
- User must complete login quickly
- Implement retry UI

---

## Scenario 7: Network/Firewall

### Break
- Django cannot reach Keycloak

### Symptom
```
Error: Connection refused
```

### Diagnosis
1. Check network connectivity
2. Verify Keycloak URL from Django container
3. Check firewall rules

### Fix
- Ensure Keycloak accessible from Django
- Check docker network

---

## Scenario 8: User Not in Keycloak

### Break
- User doesn't exist in Keycloak

### Symptom
```
Error: Invalid user credentials
```

### Diagnosis
1. Verify user exists in Keycloak
2. Check user is enabled
3. Verify user has email

### Fix
- Create user in Keycloak
- Set password
- Enable user

---

## Quick Reference

| Scenario | Symptom | Fix |
|----------|---------|-----|
| Redirect URI | Error on Keycloak | Match exactly |
| Client Secret | invalid_client | Copy from Keycloak |
| SameSite | Session lost | Set SESSION_COOKIE_SAMESITE |
| Issuer | Token validation fail | Check realm name |
| is_staff | 403 on /admin/ | Map admin role |
| Code expired | invalid_grant | Retry quickly |
| Network | Connection refused | Check connectivity |
| No user | Invalid credentials | Create user |
