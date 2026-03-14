# System Architecture — Wagtail + Keycloak SSO

## Stack Overview

```
┌─────────┐     ┌─────────┐     ┌───────────┐     ┌─────────┐
│ Browser │ ──► │ Django  │ ──► │allauth   │ ──► │Keycloak│
│         │ ◄── │ +Wagtail│ ◄── │ OIDC     │ ◄── │  (IdP) │
└─────────┘     └─────────┘     └───────────┘     └─────────┘
      │              │                │
      │              ▼                ▼
      │         ┌─────────┐     ┌─────────┐
      │         │Session  │     │  JWKS   │
      │         │ Cookie  │     │ Endpoint│
      │         └─────────┘     └─────────┘
      │
      ▼
┌─────────────────┐
│ Wagtail Admin   │
│ (protected)     │
└─────────────────┘
```

## Components

| Component | Role |
|----------|------|
| Browser | User interface, cookie storage |
| Django | Web framework, session management |
| Wagtail | CMS, protected admin area |
| django-allauth | OAuth2/OIDC integration |
| Keycloak | Identity Provider (IdP) |

## Auth Flow

```mermaid
sequenceDiagram
    participant U as User
    participant B as Browser
    participant D as Django/Wagtail
    participant K as Keycloak

    B->>D: GET /admin/ (not authenticated)
    D->>B: 302 → Keycloak

    B->>K: GET /auth?client_id=...&redirect_uri=...&state=...&scope=openid
    K->>K: User authenticates

    K->>B: 302 → callback?code=...&state=...
    B->>D: GET callback

    D->>K: POST /token (code, client_id, client_secret)
    K->>D: {access_token, id_token}

    D->>K: GET /userinfo (with access_token)
    K->>D: {sub, email, name, roles}

    D->>D: Create/update user, set session
    D->>B: Set cookie, redirect to /admin/
    B->>D: GET /admin/
    D->>B: 200 OK - Admin dashboard
```

## Keycloak Configuration

### Realm
- Name: demo-realm
- Purpose: Isolated security domain

### Client
- Client ID: wagtail-demo
- Type: confidential (requires client secret)
- Protocol: openid-connect
- Authentication: client_secret_basic

### Redirect URIs
```
http://localhost:8000/accounts/oidc/keycloak/login/callback/
http://127.0.0.1:8000/accounts/oidc/keycloak/login/callback/
```

## User Provisioning Model

```mermaid
flowchart TD
    A[SSO Login] --> B{User exists?}
    B -->|No| C[Create new user]
    B -->|Yes| D[Update existing user]
    C --> E[Set email from Keycloak]
    D --> E
    E --> F{Is admin role?}
    F -->|Yes| G[Set is_staff=True]
    F -->|No| H[Set is_staff=False]
    G --> I[Save user]
    H --> I
    I --> J[Create session]
```

### Adapter Logic
```python
def populate_user(self, request, sociallogin, data):
    user = super().populate_user(request, sociallogin, data)
    user.email = data.get('email')
    # Map admin role
    roles = data.get('realm_access', {}).get('roles', [])
    if 'admin' in roles:
        user.is_staff = True
        user.is_superuser = True
    return user
```

## Session Lifecycle

```mermaid
stateDiagram-v2
    [*] --> NotAuthenticated
    NotAuthenticated --> Authenticating: SSO login initiated
    Authenticating --> TokenExchange: User credentials valid
    TokenExchange --> UserProvisioned: Token validated
    UserProvisioned --> Authenticated: Session created
    Authenticated --> NotAuthenticated: Logout
    Authenticated --> [*]: Session expired
```

## Key Endpoints

| Endpoint | Purpose |
|----------|---------|
| `/admin/` | Wagtail admin (protected) |
| `/accounts/oidc/keycloak/login/` | Initiate SSO |
| `/accounts/oidc/keycloak/login/callback/` | OIDC callback |
| `/auth/realms/{realm}/.well-known/openid-configuration` | OIDC discovery |
| `/auth/realms/{realm}/protocol/openid-connect/certs` | JWKS |
| `/auth/realms/{realm}/protocol/openid-connect/token` | Token exchange |

## Security Settings

### Django (Django 4.x)
- SESSION_COOKIE_SAMESITE = 'Lax'
- SESSION_COOKIE_SECURE = True (production)
- CSRF_COOKIE_SAMESITE = 'Lax'

### Keycloak
- Client authentication: client_secret_basic
- Access token lifespan: 300 seconds
- SSO session idle: 1800 seconds
