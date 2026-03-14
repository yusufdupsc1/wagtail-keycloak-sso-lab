# Interview Cheatsheet — Wagtail + Keycloak SSO

---

## 30-Second Pitch

> "I debugged a production SSO failure between Wagtail and Keycloak. Multiple failure points stacked — redirect URI, token exchange, session, staff mapping. I traced the full OIDC flow, identified each break, and fixed it. I don't just configure SSO — I debug it when it breaks."

---

## Technical Q&A

### Q1: How does OAuth2 Authorization Code flow work?

**Answer:**
1. App redirects to Keycloak with client_id, redirect_uri, state
2. User authenticates on Keycloak
3. Keycloak redirects back with authorization code
4. App exchanges code for access_token + id_token
5. App validates token, creates session

---

### Q2: What is OIDC vs OAuth2?

**Answer:**
- OAuth2 = authorization (what can you access?)
- OIDC = authentication + identity layer on OAuth2
- OIDC adds: ID token, userinfo endpoint, standard scopes (openid, email, profile)

---

### Q3: What's the most common SSO failure?

**Answer:**
Redirect URI mismatch. Keycloak expects exact match. Trailing slash, protocol, domain — any difference = failure.

---

### Q4: How do you debug SSO login failure?

**Answer:**
1. Ask: does error happen before or after Keycloak login?
2. Enable debug logging on both sides
3. Trace the OAuth2 flow step by step
4. Check each configuration point
5. Fix the specific break

---

### Q5: What does the custom adapter do?

**Answer:**
Handles user creation and role mapping. Keycloak user → Django user. Maps Keycloak roles (admin/editor) → Django permissions (is_staff, is_superuser).

---

### Q6: Why Django 4.x SSO issues?

**Answer:**
Django 4.0+ changed SameSite cookie defaults. If not configured correctly, session doesn't persist after login.

---

### Q7: What is JWKS?

**Answer:**
JSON Web Key Set. Public keys from Keycloak. Django uses them to verify JWT token signatures.

---

### Q8: What is state parameter?

**Answer:**
CSRF protection. Random string generated at login start, validated at callback. Prevents cross-site request forgery.

---

## Code Snippets

### Custom Adapter
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

### Debug Settings
```python
LOGGING = {
    'version': 1,
    'loggers': {
        'allauth': {'level': 'DEBUG'},
    },
}
```

---

## Red Flags to Mention

- "SSO works in dev, breaks in prod" → Check SameSite/secure cookies
- "Users can login but can't access admin" → Check is_staff mapping
- "Works for some users" → Check Keycloak user status/roles

---

## What This Proves

- ✅ Production debugging methodology
- ✅ OIDC/OAuth2 protocol understanding
- ✅ Django auth internals
- ✅ Keycloak administration
- ✅ Multi-layer failure analysis
- ✅ Client communication
