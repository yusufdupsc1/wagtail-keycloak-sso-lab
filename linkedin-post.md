# LinkedIn Post

---

Wagtail upgrade broke Keycloak SSO. Multiple failure points stacked:

1. Redirect URI mismatch after upgrade
2. Token validation failure
3. User staff mapping broken

Systematic debugging across full OIDC flow identified each break and fixed it.

What this proves:
- Production debugging methodology
- OIDC protocol understanding
- Django auth internals

Debug artifacts: github.com/yusufdupsc1/wagtail-keycloak-sso-lab

#SSO #OIDC #Keycloak #Django #Wagtail #Backend #Engineering
