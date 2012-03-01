#!/usr/bin/env python
import sys
from coverage import coverage
from optparse import OptionParser

from django.conf import settings

if not settings.configured:
    settings.configure(
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    }
                },
            INSTALLED_APPS=[
                'django.contrib.auth',
                'django.contrib.admin',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.sites',
                'styleguide',
                ],
            DEBUG=False,
            SITE_ID=1,
            STYLEGUIDE_PATH='/tmp',
        )

from django.test.simple import DjangoTestSuiteRunner


def run_tests(*test_args):

    if not test_args:
        test_args = ['styleguide']

    # Run tests
    test_runner = DjangoTestSuiteRunner(verbosity=2)

    c = coverage(source=['styleguide'], omit=['*tests*', ])
    c.start()
    num_failures = test_runner.run_tests(test_args)
    c.stop()

    if num_failures > 0:
        sys.exit(num_failures)
    print "Generating HTML coverage report"
    c.html_report()


if __name__ == '__main__':
    parser = OptionParser()
    (options, args) = parser.parse_args()
    run_tests(*args)
