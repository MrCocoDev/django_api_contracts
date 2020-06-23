import logging

log = logging.getLogger(__name__)


def get_contract(request, request_contract, pass_in_user=False):
    if pass_in_user:
        return request_contract(request.data, request.user)
    else:
        return request_contract(request.data)


def apply_response_contract(request, response_data, pass_in_user=False):
    if pass_in_user:
        contract = request.contracts['response'](user=request.user, data=response_data)
    else:
        contract = request.contracts['response'](data=response_data)

    if contract.errors:
        log.error("Response from %s did not adhere to its contract", request.url, extra={"data": {"request": request}})

    return contract.cleaned_data
