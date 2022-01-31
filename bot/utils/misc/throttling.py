def rate_limit(key="default"):
    def decorator(func):
        setattr(func, 'throttling_key', key)
        return func
    return decorator
