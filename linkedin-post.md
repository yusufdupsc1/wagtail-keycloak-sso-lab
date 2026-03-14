# LinkedIn Post

---

Wagtail upgrade broke Keycloak SSO. Multiple failure points stacked — redirect URI drift, SameSite cookie changes in Django 4, adapter incompatibility.

Systematic debugging across the full OIDC flow identified each break and fixed it.

**What this proves:**
- Protocol-level debugging (OIDC/OAuth2)
- Django auth internals
- Production debugging methodology

Debug artifacts and working lab:

github.com/yusufdupsc1/wagtail-keycloak-sso-lab

#SSO #OIDC #Keycloak #Django #Wagtail #Backend #Engineering
