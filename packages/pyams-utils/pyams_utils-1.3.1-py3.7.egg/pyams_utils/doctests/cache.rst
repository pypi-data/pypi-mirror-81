
========================
PyAMS_utils cache module
========================

This module is used to provide a few helpers related to cache management ; the ICacheKey
interface is used to get a cache key value for any object:

    >>> from pyramid.testing import setUp, tearDown, DummyRequest
    >>> config = setUp(hook_zca=True)
    >>> config.registry.settings['zodbconn.uri'] = 'memory://'

    >>> from pyramid_zodbconn import includeme as include_zodbconn
    >>> include_zodbconn(config)
    >>> from pyams_utils import includeme as include_utils
    >>> include_utils(config)

    >>> from pyams_utils.zodb import ZODBConnection
    >>> from pyams_utils.tests import MyTestContent

    >>> import transaction
    >>> conn = ZODBConnection()
    >>> content = MyTestContent()

    >>> from pyams_utils.interfaces import ICacheKeyValue
    >>> ICacheKeyValue(content)
    '...'
    >>> int(ICacheKeyValue(content)) > 1
    True

    >>> with conn as root:
    ...     root['content'] = content
    ...     transaction.commit()

    >>> ICacheKeyValue(content)
    '1'

A TALES extension is also available to get a cache key from a Chameleon template:

    >>> request = DummyRequest(context=content)
    >>> from pyams_utils.interfaces.tales import ITALESExtension
    >>> extension = config.registry.getMultiAdapter((content, request, None), ITALESExtension,
    ...                                             name='cache_key')
    >>> extension.render()
    '1'
    >>> extension.render(content)
    '1'


Tests cleanup:

    >>> tearDown()
