# SSO Triage Checklist

> Operational debugging guide. Check each box.

---

## Phase 1: Information Gathering

- [ ] Collect error message
- [ ] Determine failing stage (1-7)
- [ ] Get Keycloak URL
- [ ] Get realm name
- [ ] Get client ID
- [ ] Get Django DEBUG=True

---

## Phase 2: Redirect Configuration

### Keycloak Side
- [ ] Valid Redirect URIs listed
- [ ] Each URI matches Django EXACTLY
- [ ] Trailing slash consistent
- [ ] Protocol matches (http/https)

### Django Side
- [ ] SOCIALACCOUNT_PROVIDERS configured
- [ ] KEYCLOAK_URL ends with /auth/
- [ ] KEYCLOAK_REALM matches

---

## Phase 3: OIDC Discovery

- [ ] Discovery endpoint accessible:
  ```
  https://{keycloak}/auth/realms/{realm}/.well-known/openid-configuration
  ```
- [ ] authorization_endpoint present
- [ ] token_endpoint present
- [ ] userinfo_endpoint present
- [ ] jwks_uri present

---

## Phase 4: Client Credentials

- [ ] Client ID in Django matches Keycloak
- [ ] Client secret in Django matches Keycloak
- [ ] Client enabled in Keycloak
- [ ] Client protocol: openid-connect
- [ ] Authentication flow: Standard

---

## Phase 5: State / Nonce

### Request to Keycloak
- [ ] client_id present
- [ ] redirect_uri present
- [ ] response_type=code
- [ ] scope includes openid
- [ ] state parameter generated

### Callback from Keycloak
- [ ] code parameter present
- [ ] state parameter present
- [ ] state matches original

---

## Phase 6: Token Exchange

### POST to Keycloak
- [ ] grant_type=authorization_code
- [ ] client_id sent
- [ ] client_secret sent
- [ ] code sent
- [ ] redirect_uri sent

### Response
- [ ] HTTP 200
- [ ] access_token present
- [ ] id_token present
- [ ] token_type=Bearer
- [ ] expires_in present

---

## Phase 7: JWKS Verification

- [ ] JWKS endpoint accessible:
  ```
  https://{keycloak}/auth/realms/{realm}/protocol/openid-connect/certs
  ```
- [ ] Returns valid JSON
- [ ] Keys array present
- [ ] Django can fetch keys

---

## Phase 8: ID Token Validation

- [ ] iss matches Keycloak URL
- [ ] aud matches client_id
- [ ] exp not passed
- [ ] iat not in future
- [ ] sub (subject) present
- [ ] Signature verified

---

## Phase 9: Session Cookie

- [ ] SESSION_COOKIE_SAMESITE configured (Lax/None)
- [ ] SESSION_COOKIE_SECURE (production)
- [ ] Cookie set after login
- [ ] Cookie sent with requests

---

## Phase 10: Proxy Headers

- [ ] SECURE_PROXY_SSL_HEADER configured (if behind proxy)
- [ ] USE_X_FORWARDED_HOST=True (if applicable)
- [ ] Proxy passes X-Forwarded-Proto

---

## Phase 11: User Provisioning

- [ ] User exists in Keycloak
- [ ] User enabled in Keycloak
- [ ] User has email in Keycloak

### Adapter Check
- [ ] SOCIALACCOUNT_ADAPTER configured
- [ ] Adapter is_open_for_signup returns True

---

## Phase 12: Staff / Admin Role Mapping

- [ ] User created in Django after SSO
- [ ] User has is_staff=True OR
- [ ] Adapter maps Keycloak role to is_staff

### Test
- [ ] User can access /admin/
- [ ] User has correct permissions

---

## Phase 13: Logout

- [ ] Logout URL works
- [ ] Session destroyed
- [ ] User redirected to login

---

## Quick Decision Tree

```
Error happens?
  │
  ├─ Before Keycloak → Redirect URI
  ├─ On Keycloak → Credentials
  ├─ After callback → Token exchange
  ├─ After token → User provisioning
  ├─ After login → Session cookie
  └─ At admin → is_staff mapping
```

---

## Debug Commands

```bash
# Test Keycloak discovery
curl https://keycloak/auth/realms/{realm}/.well-known/openid-configuration

# Test JWKS
curl https://keycloak/auth/realms/{realm}/protocol/openid-connect/certs

# Django users
docker compose exec django python manage.py shell
from django.contrib.auth import get_user_model
User = get_user_model()
print(User.objects.count())

# Social accounts
from allauth.socialaccount.models import SocialAccount
print(SocialAccount.objects.count())
```

---

## Common Fixes

| Issue | Fix |
|-------|-----|
| redirect_uri_mismatch | Match exactly in Keycloak |
| invalid_client | Copy client secret |
| User not created | Add is_open_for_signup adapter |
| 403 on /admin | Map admin role to is_staff |
| Session lost | Check SAMESITE=Lax |
