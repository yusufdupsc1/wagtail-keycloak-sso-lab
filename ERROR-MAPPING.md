# Error Mapping — Wagtail + Keycloak SSO

| Error | Cause | Fix |
|-------|-------|-----|
| redirect_uri_mismatch | URI in Keycloak ≠ Django callback | Match exactly |
| invalid_client | Wrong client ID or secret | Copy from Keycloak |
| invalid_grant | Code expired or used | Retry fresh login |
| User not created | Adapter missing | Add is_open_for_signup |
| 403 on /admin | No is_staff | Map Keycloak role |
| Session lost | SameSite cookie | Configure SAMESITE=Lax |
| Token validation failed | JWKS not reachable | Check network/firewall |
