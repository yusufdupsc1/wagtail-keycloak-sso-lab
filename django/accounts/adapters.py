"""
Custom Social Account Adapter for Keycloak SSO.
Maps Keycloak roles to Django staff/superuser.
"""

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class KeycloakSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Adapter to handle Keycloak user creation and role mapping.
    """
    
    def is_open_for_signup(self, request, sociallogin):
        """Allow new users to sign up via Keycloak SSO."""
        return True
    
    def populate_user(self, request, sociallogin, data):
        """
        Populate user fields from Keycloak claims.
        Map Keycloak roles to Django staff/superuser.
        """
        user = super().populate_user(request, sociallogin, data)
        
        # Map Keycloak claims to Django fields
        user.first_name = data.get('given_name', '')
        user.last_name = data.get('family_name', '')
        
        # Get roles from Keycloak token
        realm_access = data.get('realm_access', {})
        roles = realm_access.get('roles', [])
        
        # Map admin role to Django staff
        if 'admin' in roles:
            user.is_staff = True
            user.is_superuser = True
        
        return user
