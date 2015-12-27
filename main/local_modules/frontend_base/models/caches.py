import logging

from cachetools import TTLCache

_logger = logging.getLogger(__name__)

# caches are named after the length of their cycle.
# cache_1h is automatically cleared every hour, etc.
caches = {
    'cache_1h': TTLCache(100, 3600),
    'cache_3h': TTLCache(100, 10800),
}


def clear_caches():
    """clear all the caches.

    :return: number cache cleared.
    """
    count = 0

    for cache in caches.itervalues():
        cache.clear()
        count += 1

    _logger.debug('%d cache(s) cleared', count)
    return count
