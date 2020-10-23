import base64

from .oauth import BaseOAuth2

class CleverOAuth2(BaseOAuth2):
    """
    Clever OAuth2 authentication backend
    Doc Reference: https://marketplace.zoom.us/docs/guides/auth/oauth
    """

    name = 'clever-oauth2'
    ID_KEY = 'client_id'
    AUTHORIZATION_URL = 'https://clever.com/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://clever.com/oauth/tokens'
    USER_DETAILS_URL = 'https://api.clever.com/v2.0/me'
    DEFAULT_SCOPE = ['user:read']
    ACCESS_TOKEN_METHOD = 'POST'
    REFRESH_TOKEN_METHOD = 'POST'
    REDIRECT_STATE = False

    def user_data(self, access_token, *args, **kwargs):
        import ipdb; ipdb.set_trace()
        response = self.get_json(
            self.USER_DETAILS_URL, headers={
                'Authorization': 'Bearer {access_token}'.format(access_token=access_token)
            }
        )
        return response

    def get_redirect_uri(self, state=None):
        import ipdb; ipdb.set_trace()
        response = super().get_redirect_uri(state)
        return response

    def get_user_details(self, response):
        import ipdb; ipdb.set_trace()
        username = response.get('id', '')
        first_name = response.get('first_name', '')
        last_name = response.get('last_name', '')
        email = response.get('email', '')
        fullname = ''
        return {
            'username': username,
            'email': email,
            'fullname': fullname,
            'first_name': first_name,
            'last_name': last_name,
        }

    def auth_complete_params(self, state=None):
        import ipdb; ipdb.set_trace()
        state["client_id"] = '5a7a8821db09037d6082'
        return {
            'grant_type': 'authorization_code',  # request auth code
            'code': self.data.get('code', ''),  # server response code
            'redirect_uri': self.get_redirect_uri(state),
        }

    def auth_headers(self):
        import ipdb; ipdb.set_trace()
        return {
            'Authorization': b'Basic ' + base64.urlsafe_b64encode(
                '{0}:{1}'.format(*self.get_key_and_secret()).encode()
            )
        }

    def refresh_token_params(self, token, *args, **kwargs):
        import ipdb; ipdb.set_trace()
        return {'refresh_token': token, 'grant_type': 'refresh_token'}
