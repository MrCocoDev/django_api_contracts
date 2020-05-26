from functools import wraps
from logging import getLogger

log = getLogger(__name__)


def apply_response(contract):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
        wrapper.response_contract = contract
        return wrapper
    return decorator


def response_contract(response_data, view, contract=None):
    if not contract:
        contract = view.response_contract

    contract = contract(response_data)
    if contract.errors:
        log.error(
            msg=f"Response contract was broken by {view.__name__}!",
            extra={
                'data': response_data,
                'contract': contract,
            }
        )

    return contract.cleaned_data



