from django.contrib.auth import authenticate
from wsgidav.wsgidav_app import DEFAULT_CONFIG
from wsgidav.wsgidav_app import WsgiDAVApp
from .settings import DAV_ROOT, PROVIDER_NAME
from .models import ResourceAccess


class TemplationDomainController(object):
    def requireAuthentication(self, realmname, environ):
        return True

    def getDomainRealm(self, inputRelativeURL, environ):
        return environ.get('PATH_INFO').split('/')[1]

    def authDomainUser(self, realmname, username, password, environ):
        user = authenticate(username=username, password=password)
        try:
            return ResourceAccess.objects.get(user=user, resource__id=realmname)
        except ResourceAccess.DoesNotExist:
            return False

config = DEFAULT_CONFIG.copy()
config['provider_mapping'][PROVIDER_NAME] = DAV_ROOT
config['user_mapping'][DAV_ROOT] = {None: None}
config['domaincontroller'] = TemplationDomainController()
config['acceptdigest'] = False
config['defaultdigest'] = False

wsgidav_app = WsgiDAVApp(config)


class WsgiDAVMiddleware(object):
    def __init__(self, django_app):
        self.django_app = django_app

    def __call__(self, environ, start_response):
        if environ.get('PATH_INFO').startswith('/' + PROVIDER_NAME):
            return wsgidav_app(environ, start_response)
        return self.django_app(environ, start_response)
