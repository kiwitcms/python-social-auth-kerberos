import base64
import gssapi

from social_core.backends.base import BaseAuth
from social_core.exceptions import AuthException


class KerberosAuth(BaseAuth):
    _krb5 = {}
    name = 'kerberos'

    def start(self):
        response = self.strategy.html('Authorization Required')
        response.status_code = 401
        response['WWW-Authenticate'] = 'Negotiate'

        # keep a reference to the current user b/c
        # kerberos is a stateful protocol while HTTP is stateless
        if self.strategy.request.session.get('_krb5', None) is None:
            context_id = "%d@%d" % (hash(repr(self.strategy.request.META)),
                                    id(self.strategy.request))
            self.strategy.request.session['_krb5'] = context_id
            self._krb5[context_id] = None

        # if browser didn't send negotiation token ask it to send one
        if 'HTTP_AUTHORIZATION' not in self.strategy.request.META:
            return response

        token = self.strategy.request.META['HTTP_AUTHORIZATION']
        negotiate, token = token.split(' ')
        if negotiate.lower() != 'negotiate':
            raise AuthException(self.name, 'Negotiate scheme not found')
        token = base64.b64decode(token.strip())

        context_id = self.strategy.request.session.get('_krb5', None)
        if self._krb5[context_id] is None:
            keytab_path = self.strategy.setting('SOCIAL_AUTH_KRB5_KEYTAB')
            creds = gssapi.Credentials(usage='accept',
                                       store={'keytab': keytab_path})
            self._krb5[context_id] = gssapi.SecurityContext(creds=creds)

        server_token = self._krb5[context_id].step(token)
        response = self.strategy.redirect(self.redirect_uri)

        if server_token is not None:
            server_token_hex = base64.b64encode(server_token).decode()
            response['WWW-Authenticate'] = 'Negotiate %s' % server_token_hex

        return response

    def auth_complete(self, *args, **kwargs):
        """Completes loging process, must return user instance"""
        try:
            context_id = self.strategy.request.session.get('_krb5', None)

            if context_id not in self._krb5:
                raise AuthException(self.name, 'Authentication failed. context_id not found!')

            if not self._krb5[context_id].complete:
                raise AuthException(self.name, 'Authentication failed')

            kwargs.update({
                'response': {
                    'krb5_initiator': str(self._krb5[context_id].initiator_name),
                },
                'backend': self,
            })
        finally:
            if context_id in self._krb5:
                del self._krb5[context_id]

            if '_krb5' in self.strategy.request.session:
                del self.strategy.request.session['_krb5']

        return self.strategy.authenticate(*args, **kwargs)

    def auth_allowed(self, response, details):
        """Return True if the user should be allowed to authenticate"""
        return 'krb5_initiator' in response

    def get_user_id(self, details, response):
        """Return a unique ID for the current user, by default from server
        response."""
        return response['krb5_initiator']

    def get_user_details(self, response):
        """Return user details"""
        email = response['krb5_initiator'].split('/')[-1].lower()
        username = email.split('@')[0]

        return {
            'username': username,
            'email': email,
            'fullname': '',
            'first_name': '',
            'last_name': ''
        }
