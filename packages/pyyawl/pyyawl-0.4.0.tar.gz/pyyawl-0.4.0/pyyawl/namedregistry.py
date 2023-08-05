from typing import Dict, Any
import inspect
Function = Any

registry: Dict[str, Function] = dict()


def export(*arg, **kwargs):
    """decorator to export functions in the registry
    """

    def export_inner(func):
        name = kwargs['name']
        del kwargs['name']
        kwargs['func'] = func
        kwargs['arguments'] = str(inspect.signature(func))
        registry[name] = kwargs

    return export_inner


if __name__ == "__main__":
    test_name = 'sum'

    @export(name=test_name)
    def func_sum(a, b):
        return a + b

    print(registry[test_name](2, 3))
