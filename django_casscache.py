"""
django_casscache
~~~~~~~~~~~~~~~~

:copyright: (c) 2013 by Matt Robenolt.
:license: BSD, see LICENSE for more details.
"""

from django.core.cache.backends.memcached import BaseMemcachedCache


class CasscacheCache(BaseMemcachedCache):
    "An implementation of a cache binding using casscache"
    def __init__(self, server, params):
        import casscache
        super(CasscacheCache, self).__init__(server, params,
                                             library=casscache,
                                             value_not_found_exception=ValueError)

    @property
    def _cache(self):
        if getattr(self, '_client', None) is None:
            keyspace = self._options.pop('keyspace')
            columnfamily = self._options.pop('columnfamily')
            self._client = self._lib.Client(self._servers,
                                            keyspace=keyspace,
                                            columnfamily=columnfamily,
                                            **self._options)
        return self._client

    def _get_memcache_timeout(self, timeout):
        return timeout or 0

    def close(self, **kwargs):
        # Lol, Django wants to close the connection after every request.
        # This is 100% not needed for Cassandra.
        pass
