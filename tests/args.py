def a(a=None, *args, **kwargs):
    print(*args)
    print(kwargs)

print(a(1, count=1)) 