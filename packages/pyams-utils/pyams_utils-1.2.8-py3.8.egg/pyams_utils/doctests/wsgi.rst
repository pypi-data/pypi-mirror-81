
=======================
PyAMS_utils wsgi module
=======================

The "wsgi_environ_cache" can be used to cache a method result into request environment:

    >>> import pprint

    >>> from pyramid.testing import setUp, tearDown, DummyRequest
    >>> config = setUp()

    >>> from pyams_utils.wsgi import wsgi_environ_cache
    >>> class MyUtility:
    ...
    ...     @wsgi_environ_cache('MyKey')
    ...     def get_value(self, request):
    ...         pprint.pprint("Getting value...")
    ...         return 1

    >>> request = DummyRequest()

    >>> utility = MyUtility()
    >>> utility.get_value(request)
    'Getting value...'
    1

    >>> utility.get_value(request)
    1

    >>> request.environ.get('MyKey')
    1


Tests cleanup:

    >>> tearDown()
