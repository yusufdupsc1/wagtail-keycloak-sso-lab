# Upwork Proposal Pack

---

## 1. Concise Proposal (<180 words)

Subject: Quick diagnosis — I've fixed this exact issue

Hi,

I've debugged SSO failures in production apps. Your symptoms — Wagtail upgrade broke Keycloak SSO — usually come from one of five issues:

1. Redirect URI mismatch
2. Token validation failure
3. Session cookie configuration
4. User provisioning/staff mapping
5. django-allauth adapter incompatibility

I can diagnose in under 30 minutes.

My approach:
- Trace the OIDC flow end-to-end
- Identify exact failure point
- Fix configuration or adapter
- Verify user gets admin access

Quick question: Does the error happen before or after Keycloak login?

I have 5+ years building auth systems. I find what breaks and fix it.

Best,
Yusuf

---

## 2. Premium Proposal (<250 words)

Subject: Wagtail + Keycloak SSO debugging — available now

Hi,

SSO failures after framework upgrades are frustrating. Users can't log in and you don't know why.

I've diagnosed and fixed this exact problem before.

**Common causes in your stack:**

- Redirect URI mismatch (Wagtail paths changed in 7.x)
- django-allauth provider configuration drift
- Django 4.x SameSite cookie defaults breaking sessions
- User provisioned but missing is_staff for admin access
- Custom adapter incompatible with django-allauth 65.x

**My diagnostic approach:**

1. Identify which of the 5 failure buckets you're in
2. Enable debug logging on Django and Keycloak
3. Trace the OIDC authorization code flow
4. Fix the specific broken link
5. Verify user gets Wagtail admin access

**What I've built:**

- Working Django + Wagtail + Keycloak lab
- Debug artifacts and triage checklists
- Failure scenario documentation

GitHub: github.com/yusufdupsc1/wagtail-keycloak-sso-lab

Can you share the exact error message? That will help narrow down the cause.

Best,
Yusuf

---

## 3. Two-Sentence Opener

**Version A:**
> "I've debugged SSO failures after Wagtail upgrades. The issue is usually one of five things — I can identify which and fix it."

**Version B:**
> "I specialize in production authentication debugging. Wagtail + Keycloak SSO issues are my specialty."

---

## Context for Proposals

- **Role:** Backend Engineer
- **Specialty:** Auth systems, payments, SSO
- **GitHub:** github.com/yusufdupsc1
- **Stack:** Django, Wagtail, Keycloak, Stripe
