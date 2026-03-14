# SSO Debug Report Template

---

## 1. Environment

### Client Environment
| Field | Value |
|-------|-------|
| Wagtail Version | |
| Django Version | |
| django-allauth Version | |
| Keycloak Version | |
| Python Version | |
| Database | |

### Configuration
| Setting | Value |
|---------|-------|
| Keycloak URL | |
| Realm | |
| Client ID | |
| Redirect URI | |
| ALLOWED_HOSTS | |

---

## 2. Reproduction Steps

```
1.
2.
3.
4.
5.
```

### Expected Behavior
[What should happen]

### Actual Behavior
[What actually happened]

---

## 3. Failing Stage

| # | Stage | Status |
|---|-------|--------|
| 1 | Redirect to Keycloak | ☐ Pass / ☐ Fail |
| 2 | Keycloak Login | ☐ Pass / ☐ Fail |
| 3 | Callback Return | ☐ Pass / ☐ Fail |
| 4 | Token Exchange | ☐ Pass / ☐ Fail |
| 5 | User Provisioning | ☐ Pass / ☐ Fail |
| 6 | Session Creation | ☐ Pass / ☐ Fail |
| 7 | Admin Access | ☐ Pass / ☐ Fail |

**Failing at stage:** [ ]

---

## 4. Evidence

### Error Message
```
[Exact error message]
```

### URL at Failure
```
[Full URL including parameters]
```

### Keycloak Logs
```
[Paste relevant Keycloak log entries]
```

### Django Logs
```
[Paste relevant Django log entries]
```

### Browser Console
```
[Any JavaScript errors]
```

---

## 5. Root Cause

### Primary Cause
[What actually broke]

### Contributing Factors
1.
2.
3.

### Evidence Supporting Diagnosis
- [ ]
- [ ]

---

## 6. Patch Strategy

### Immediate Fix
```python
# Code changes required
```

### Configuration Changes
```yaml
# Settings changes
```

### Verification Steps
- [ ] Test SSO login flow
- [ ] Verify user created
- [ ] Verify staff access
- [ ] Test logout

---

## 7. Regression Risk

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| | | | |

---

## 8. Verification Checklist

- [ ] SSO login works end-to-end
- [ ] User created in Django
- [ ] User has correct permissions
- [ ] Admin access works
- [ ] Logout works
- [ ] Session persists across requests
- [ ] No errors in logs

---

## 9. Prevention

### Monitoring
- [ ] Add SSO failure alert
- [ ] Log token exchange success/failure

### Documentation
- [ ] Update runbook
- [ ] Document configuration

### Testing
- [ ] Add integration test for SSO
- [ ] Add regression test for this bug

---

## 10. Timeline

| Phase | Time |
|-------|------|
| Diagnosis | |
| Fix Implementation | |
| Testing | |
| Deployment | |
| Verification | |

**Total:** 

---

## Sign-off

| Role | Name | Date |
|------|------|------|
| Engineer | | |
| Reviewer | | |
| QA | | |
