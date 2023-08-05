# django-sentinel
Plugin for django-redis that supports Redis Sentinel. This is fork of [lamoda/django-sentinel](https://github.com/lamoda/django-sentinel) deprecated project.

# Installation

```
pip install django-sentinel-sifter
```

# Usage

Location format: master_name/sentinel_server:port,sentinel_server:port/db_id

In your settings, do something like this:

```
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis_master/sentinel-host1:2639,sentinel-host2:2639/0"
            "OPTIONS": {
                "PASSWORD": 's3cret_passw0rd!',
                "CLIENT_CLASS": "django_sentinel.SentinelClient",
            }
        }
    }
```
