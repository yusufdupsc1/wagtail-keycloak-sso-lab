# Upwork Proposal Pack

---

## 1. Concise Proposal

Subject: Wagtail + Keycloak SSO — available now

Hi,

I specialize in SSO debugging for Django/Wagtail + Keycloak stacks.

Your issue — SSO broke after Wagtail upgrade — is a known failure mode. I can identify the root cause within the first 30 minutes.

My approach: trace the OIDC flow, identify which layer is breaking, fix it.

Recent work: github.com/yusufdupsc1/wagtail-keycloak-sso-lab

Can you share the error message? That tells me exactly where to look.

Best,
Yusuf

---

## 2. Premium Proposal

Subject: Wagtail + Keycloak SSO recovery — available now

Hi,

I've recovered SSO integrations after framework upgrades for multiple clients. The symptoms are consistent: broken redirect URIs, drifting configuration, or session cookie changes.

Your stack (Wagtail 7.x + Django 4.2 + Keycloak 11) has specific failure points I'm familiar with:

- Redirect URI paths changed in Wagtail 7.x
- Django 4.x SameSite defaults broke session persistence
- django-allauth 65.x adapter changes
- User provisioned but missing is_staff for admin

I don't guess. I trace the flow and fix what's actually broken.

Portfolio: github.com/yusufdupsc1/wagtail-keycloak-sso-lab

Send me the error and I'll tell you exactly what's wrong.

Best,
Yusuf

---

## 3. Two-Sentence Opener

> "I debug production SSO failures. Wagtail + Keycloak is my specialty."
