import logging
from functools import wraps

from django_contracts.utils import get_contract
from .errors import handle_api_form_errors
from .normalizers import normalize_view_data

log = logging.getLogger(__name__)


def apply_request(request_contract, for_method='POST', pass_in_user=False):
    def decorator(func):
        wrapper = wraps(func)(_apply_request_contract(request_contract, func, pass_in_user))
        wrapper.request_contract = request_contract

        # Preserve glommed values
        for attribute in vars(func):
            if not getattr(wrapper, attribute):
                setattr(wrapper, attribute, getattr(func, attribute))

        return normalize_view_data(wrapper, for_method)

    return decorator


def _apply_request_contract(request_contract, view_function, pass_in_user=False):
    def wrapper(request, *args, **kwargs):
        contract = get_contract(request, request_contract, pass_in_user)

        if contract.errors:
            log.info(msg=f"Request has errors: {contract.errors}")
            return handle_api_form_errors(contract)

        request.contract = contract
        request.validated_data = contract.cleaned_data

        return view_function(request, *args, **kwargs)

    return wrapper
