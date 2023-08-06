from . import common_helpers
from . import builtins
from . import refs
from . import testing


def get_types():
    """Provide a list of all historian types"""
    types = list()
    types.extend(builtins.HISTORIAN_TYPES)
    types.extend(common_helpers.HISTORIAN_TYPES)
    types.extend(refs.HISTORIAN_TYPES)
    types.extend(testing.HISTORIAN_TYPES)

    return types
