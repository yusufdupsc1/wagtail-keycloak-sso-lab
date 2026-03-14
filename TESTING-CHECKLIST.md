# Wagtail SSO Lab — Testing Checklist

> Test each step. Check each box. Don't skip.

---

## Phase 1: Start Services

```bash
cd ~/Music/career-coach-ops/learning-projects/wagtail-keycloak-sso-lab

docker compose up -d --build
```

- [ ] All 3 containers start (postgres, keycloak, django)
- [ ] No errors in logs

Check:
```bash
docker compose ps
docker compose logs --tail=20
```

---

## Phase 2: Verify Keycloak

1. Open http://localhost:8080
2. Login: admin / admin
3. [ ] Admin console loads

---

## Phase 3: Configure Keycloak

### Step 3.1: Create Realm
- [ ] Click "Create realm"
- [ ] Name: `wagtail-realm`
- [ ] Click "Create"

### Step 3.2: Create Client
- [ ] Go to "Clients" → "Create"
- [ ] Client ID: `wagtail-app`
- [ ] Client Protocol: `openid-connect`
- [ ] Access Type: `confidential`
- [ ] Save

### Step 3.3: Configure Client
After saving:
- [ ] Valid Redirect URIs: 
  ```
  http://localhost:8000/accounts/keycloak/login/callback/
  http://127.0.0.1:8000/accounts/keycloak/login/callback/
  ```
- [ ] Web Origins:
  ```
  http://localhost:8000
  http://127.0.0.1:8000
  ```
- [ ] Authentication Flow: Standard Flow enabled

### Step 3.4: Get Client Secret
- [ ] Go to "Credentials" tab
- [ ] Copy the secret (we'll use it later)

### Step 3.5: Create Test User
- [ ] Go to "Users" → "Add user"
- [ ] Username: `testadmin`
- [ ] Email: `testadmin@example.com`
- [ ] First name: `Test`
- [ ] Last name: `Admin`
- [ ] Save
- [ ] Go to "Credentials" → Set password: `testpass123`
- [ ] Set "Temporary": OFF

### Step 3.6: Assign Admin Role
- [ ] Go to "Users" → testadmin → "Role mapping"
- [ ] Select "wagtail-realm" in "Client roles"
- [ ] Add: `admin` role

---

## Phase 4: Configure Django

### Step 4.1: Set Client Secret

Edit `docker-compose.yml` or create `.env`:

```bash
# Option 1: Edit docker-compose.yml
# Under django environment, add:
KEYCLOAK_CLIENT_ID: wagtail-app
KEYCLOAK_CLIENT_SECRET: 'YOUR_SECRET_HERE'

# Option 2: Create .env file
KEYCLOAK_CLIENT_ID=wagtail-app
KEYCLOAK_CLIENT_SECRET=your-secret-here
```

- [ ] Client secret set in config

### Step 4.2: Run Migrations

```bash
docker compose exec django python manage.py migrate
```

- [ ] Tables created successfully

### Step 4.3: Create Superuser

```bash
docker compose exec django python manage.py createsuperuser
```

- [ ] Superuser created (for manual admin access)

---

## Phase 5: Test SSO Login

### Step 5.1: Initiate SSO

1. Visit: http://localhost:8000/accounts/keycloak/login/
2. [ ] Redirects to Keycloak login page

### Step 5.2: Login with Keycloak

1. Enter: testadmin / testpass123
2. Click "Log in"
3. [ ] Redirects back to Django

### Step 5.3: Verify Success

- [ ] User redirected to home/dashboard
- [ ] User can access /admin/
- [ ] User has staff permissions (from adapter)

---

## Phase 6: Debug Common Issues

### Issue 1: redirect_uri_mismatch

**Check:**
- [ ] Keycloak redirect URI exactly matches Django callback
- [ ] Trailing slash consistent

**Fix:** Copy exact URI from Django settings to Keycloak

---

### Issue 2: invalid_client

**Check:**
- [ ] Client secret matches exactly
- [ ] Client ID correct

**Fix:** Copy secret from Keycloak "Credentials" tab

---

### Issue 3: User not created / Can't access admin

**Check:**
- [ ] Adapter is being used
- [ ] User has is_staff=True

**Fix:** Check adapters.py is configured in settings.py

---

## Verification Commands

```bash
# Check containers
docker compose ps

# View logs
docker compose logs -f django
docker compose logs -f keycloak

# Django shell
docker compose exec django python manage.py shell

# Check users
docker compose exec django python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
print('Users:', User.objects.count())
"
```

---

## Success Criteria

| Check | Expected |
|-------|----------|
| Keycloak starts | Yes |
| Django starts | Yes |
| SSO login works | Yes |
| User created | Yes |
| User has staff | Yes |
| Admin access | Yes |

---

## Next: After Successful Test

1. Push to GitHub
2. Create LinkedIn post
3. Apply to Upwork jobs

---

*Test each step. Check each box.*
