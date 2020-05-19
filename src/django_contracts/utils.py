

def get_contract(request, request_contract, pass_in_user=False):
    if pass_in_user:
        return request_contract(request.data, request.user)
    else:
        return request_contract(request.data)
