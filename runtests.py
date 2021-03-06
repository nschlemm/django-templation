import os
import sys

try:
    from django.conf import settings

    BASE_DIR = os.path.dirname(os.path.realpath(__file__))

    settings.configure(
        BASE_DIR=BASE_DIR,
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
            }
        },
        ROOT_URLCONF="tests.urls",
        INSTALLED_APPS=[
            "django.contrib.sessions",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.staticfiles",
            "django.contrib.sites",
            "django.contrib.admin",
            "templation",
            "tests",
        ],
        SITE_ID=1,
        NOSE_ARGS=['-s'],


        STATIC_URL='/static/',
        STATIC_ROOT=os.path.join(BASE_DIR, 'tests', 'static'),

        STATICFILES_FINDERS=(
            'templation.finders.TemplationStaticFinder',
            'django.contrib.staticfiles.finders.FileSystemFinder',
            'django.contrib.staticfiles.finders.AppDirectoriesFinder',
            # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
        ),

        TEMPLATE_LOADERS=(
            'templation.loaders.TemplationLoader',
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader'
        ),

        TEMPLATE_DIRS = (
            os.path.join(BASE_DIR, 'tests/templates'),
        ),

        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'templation.middleware.TemplationMiddleware',
        ),

        TEMPLATION_DEBUG=True,
        TEMPLATION_BOILERPLATE_FOLDER=os.path.join(BASE_DIR, 'tests', 'boilerplate'),
        TEMPLATION_DAV_ROOT='/tmp/dav/',
        TEMPLATION_DAV_STATIC_URL='/templationdav/',
        TEMPLATION_RESOURCE_MODEL='tests.models.MyResource',
        TEMPLATION_SANDBOX=True,
    )

    from django_nose import NoseTestSuiteRunner
except ImportError:
    raise ImportError("To fix this error, run: pip install -r requirements-test.txt")


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    # Run tests
    test_runner = NoseTestSuiteRunner(verbosity=1)

    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(failures)


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
