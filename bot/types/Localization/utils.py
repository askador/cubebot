from typing import Optional, Union, overload


@overload
def get(keys: str, resources: Optional[dict]) -> Optional[str]:
    ...
@overload
def get(keys: str, resources: Optional[dict]) -> Optional[list[str]]:
    ...

def get(keys, resources):
    keys = keys.split('.')

    def rec(keys, resources):
        if not resources or not len(keys) or type(resources) is not dict:
                return
        if len(keys) == 1:
            return resources.get(keys[0])
        return rec(keys[1:], resources.get(keys[0]))

    return rec(keys, resources)

