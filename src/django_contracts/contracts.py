import logging
from functools import wraps
from .request import apply_request
from .response import apply_response

log = logging.getLogger(__name__)


def request_contract(request_contracts, response_contract, pass_in_user=False):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            method = request.method
            request_contract = request_contracts[method]
            new_func = apply_response(contract=response_contract)(func=func)
            new_func = apply_request(
                request_contract=request_contract,
                for_method=method,
                pass_in_user=pass_in_user
            )(func=new_func)

            return new_func

        return wrapper

    return decorator
