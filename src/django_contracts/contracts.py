import logging
from functools import wraps
from .errors import handle_api_form_errors
from .normalizers import normalize_view_data

log = logging.getLogger(__name__)


def apply_contract(request_contracts=None, response_contracts=None, pass_in_user=False):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            errors = normalize_view_data(request)
            if errors:
                return errors

            if response_contracts:

                method = request.method
                contract_for_method = response_contracts[method]

                try:
                    request.contracts['response'] = contract_for_method
                except (AttributeError, KeyError):
                    request.contracts = {
                        'response': contract_for_method
                    }

            if request_contracts:

                method = request.method
                contract_for_method = request_contracts[method]

                if pass_in_user:
                    contract = contract_for_method(request.data, getattr(request, 'user', None))
                else:
                    contract = contract_for_method(request.data)

                if contract.errors:
                    log.info(msg=f"Request has errors: {contract.errors}")
                    return handle_api_form_errors(contract)

                try:
                    request.contracts['request'] = contract
                except (AttributeError, KeyError):
                    request.contracts = {
                        'request': contract,
                    }

                request.validated_data = contract.cleaned_data

            return func(request, *args, **kwargs)

        try:
            wrapper.contracts['response'] = response_contracts
        except (AttributeError, KeyError):
            wrapper.contracts = {
                'response': response_contracts
            }

        try:
            wrapper.contracts['request'] = request_contracts
        except (AttributeError, KeyError):
            wrapper.contracts = {
                'request': request_contracts
            }
        return wrapper

    return decorator
