from project_apps.api_tools.requests import log


def apply_response_contract(response_contract, response_data, view):
    contract = response_contract(response_data)

    if contract.errors:
        log.error(
            msg=f"Response contract was broken by {view.__name__}!",
            extra={
                'data': response_data,
                'contract': response_contract,
            }
        )

    return contract.cleaned_data
