# Upwork Proposal — SSO Debug

---

**Subject:** Quick diagnosis — I've fixed this exact issue

---

Hi,

I've debugged SSO integration failures between Wagtail/Django and Keycloak. The symptoms you're describing — users can't log in after upgrade — usually come from one of three issues:

1. Redirect URI mismatch (most common)
2. JWT token validation failing
3. User provisioning/staff mapping broken

I can't say for certain without checking, but I can diagnose in under 30 minutes.

**My approach:**
- Check Keycloak client settings against Django callback
- Enable debug logging and trace OAuth2 flow
- Identify exact failure point and fix

**Quick question:** Does the error appear immediately (redirect issue) or after Keycloak login (token/session issue)?

I have 5+ years building auth systems — payments, OAuth2, role-based access. I find what breaks and fix it.

Happy to jump on a call.

Best,
Yusuf

---

**Portfolio:** github.com/yusufdupsc1/wagtail-keycloak-sso-lab
