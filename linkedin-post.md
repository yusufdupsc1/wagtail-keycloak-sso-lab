# LinkedIn Post

---

Recovered a broken Keycloak SSO integration after Wagtail upgrade.

Root cause: multiple failure points — redirect URI drift, SameSite cookie changes in Django 4, adapter incompatibility.

The fix: systematic OIDC flow tracing, not guesswork.

Proof: github.com/yusufdupsc1/wagtail-keycloak-sso-lab

#SSO #OIDC #Keycloak #Django #Wagtail #Backend
