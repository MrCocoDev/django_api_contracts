import logging
import re
from functools import wraps

from django.shortcuts import redirect

from .errors import handle_api_form_errors
from .helpers import normalize_view_post_data, normalize_view_get_data, get_contract

log = logging.getLogger(__name__)


def apply_post_request_contract(request_contract):
    def decorator(func):

        @wraps(func)
        def wrapper(request, *args, **kwargs):
            contract = get_contract(request, request_contract)

            if contract.errors:
                return handle_api_form_errors(contract)

            request.validated_form = contract

            response = func(request, *args, **kwargs)

            if re.match(r'text/html', request.META.get('HTTP_ACCEPT', '')):
                return redirect(to='events_home_view')

            return response

        return normalize_view_post_data(wrapper)

    return decorator


def apply_get_request_contract(request_contract):
    def decorator(func):

        @wraps(func)
        def wrapper(request, *args, **kwargs):
            contract = get_contract(request, request_contract)

            if contract.errors:
                log.info(msg=f"GET request has errors: {contract.errors}")
                return handle_api_form_errors(contract)

            request.validated_form = contract

            return func(request, *args, **kwargs)
        return normalize_view_get_data(wrapper)

    return decorator
