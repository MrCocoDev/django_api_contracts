import logging
from functools import wraps
from .request import apply_request
from .response import apply_response

log = logging.getLogger(__name__)


def request_contract(request_contracts, response_contract, pass_in_user=False):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            new_func = func
            if response_contract:
                new_func = apply_response(contract=response_contract)(func=new_func)

            if request_contracts:
                method = request.method
                contract = request_contracts[method]
                new_func = apply_request(
                    request_contract=contract,
                    for_method=method,
                    pass_in_user=pass_in_user
                )(func=new_func)

            return new_func

        return wrapper

    return decorator
