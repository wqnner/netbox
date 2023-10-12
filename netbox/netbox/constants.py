# Prefix for nested serializers
NESTED_SERIALIZER_PREFIX = 'Nested'

# RQ queue names
RQ_QUEUE_DEFAULT = 'default'
RQ_QUEUE_HIGH = 'high'
RQ_QUEUE_LOW = 'low'

# Keys for PostgreSQL advisory locks. These are arbitrary bigints used by the advisory_lock
# context manager. When a lock is acquired, one of these keys will be used to identify said lock.
# When adding a new key, pick something arbitrary and unique so that it is easily searchable in
# query logs.
ADVISORY_LOCK_KEYS = {
    'available-prefixes': 100100,
    'available-ips': 100200,
    'available-vlans': 100300,
    'available-asns': 100400,

    # MPTT locks
    'region': 100500,
    'sitegroup': 100501,
    'location': 100502,
    'tenantgroup': 100503,
    'contactgroup': 100504,
    'wirelesslangroup': 100505,
    'inventoryitem': 100506,
    'inventoryitemtemplate': 100507,
}
