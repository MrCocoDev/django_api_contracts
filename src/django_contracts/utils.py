from inspect import isfunction


def get_contract(request, request_contract):
    if isfunction(request_contract):
        request_contract_actual = request_contract(request.user)
    else:
        request_contract_actual = request_contract

    return request_contract_actual(request.data)