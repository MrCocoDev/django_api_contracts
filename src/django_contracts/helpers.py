import json
from functools import wraps
from inspect import isfunction

from django import http


def normalize_view_post_data(func):
    """
    Wraps a function that is expecting a request with POST data and normalizes the POST data
    inside of `request.data` this allows views to operate without caring about the format
    of the request. If the request data cannot be normalized an error response will be
    returned to the user.

    :param func: The function to wrap
    :type func: types.FunctionType
    :return: A wrapped function which can take POST requests of all content types
    :rtype: types.FunctionType
    """
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            request.data = normalize_request_post_data(request)
        except json.JSONDecodeError as e:
            return http.HttpResponseBadRequest(
                content=json.dumps({
                    "__all__": [
                        {
                            "message":
                                f"Invalid POST data ({e}). This endpoint supports "
                                "multipart/form-data and application/json encodings",
                                "code": "invalid"
                        }
                    ]
                }),
                content_type="application/json"
            )

        return func(request, *args, **kwargs)

    return wrapper


def normalize_request_post_data(request):
    """
    Converts request.POST or a json decodable request.body into a simple python dictionary. Multiple
    form values will be converted to a list. This function has no way of knowing if a singular value
    from request.POST is intended to be an array of values of length one or not, so be prepared to
    check the type of fields that fall into that condition.

    :param request: The POST request
    :type request: django.core.handlers.wsgi.WSGIRequest
    :return: A `dict` containing the contents of the json decoded request body, or the dict representation
        of the request.POST
    :rtype: dict
    :raises: json.JSONDecodeError
    """
    body = request.body or '{}'

    # request.POST.dict() only takes a single value from array inputs so we use `lists` and transform
    # singular values back
    as_lists = request.POST.lists()
    as_mix = {key: val[0] if val and len(val) == 1 else val for key, val in as_lists}

    # If there is no request.POST try json
    post_data = as_mix or json.loads(body)

    return post_data


def normalize_view_get_data(func):
    """
    Wraps a function that is expecting a request with POST data and normalizes the POST data
    inside of `request.data` this allows views to operate without caring about the format
    of the request. If the request data cannot be normalized an error response will be
    returned to the user.

    :param func: The function to wrap
    :type func: types.FunctionType
    :return: A wrapped function which can take POST requests of all content types
    :rtype: types.FunctionType
    """
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            request.data = normalize_request_get_data(request)
        except json.JSONDecodeError as e:
            return http.HttpResponseBadRequest(
                content=json.dumps({
                    "__all__": [
                        {
                            "message":
                                f"Invalid POST data ({e}). This endpoint supports "
                                "multipart/form-data and application/json encodings",
                                "code": "invalid"
                        }
                    ]
                }),
                content_type="application/json"
            )

        return func(request, *args, **kwargs)

    return wrapper


def normalize_request_get_data(request):
    """
    Converts request.POST or a json decodable request.body into a simple python dictionary. Multiple
    form values will be converted to a list. This function has no way of knowing if a singular value
    from request.POST is intended to be an array of values of length one or not, so be prepared to
    check the type of fields that fall into that condition.

    :param request: The POST request
    :type request: django.core.handlers.wsgi.WSGIRequest
    :return: A `dict` containing the contents of the json decoded request body, or the dict representation
        of the request.POST
    :rtype: dict
    :raises: json.JSONDecodeError
    """
    body = request.body or '{}'

    # request.POST.dict() only takes a single value from array inputs so we use `lists` and transform
    # singular values back
    as_lists = request.GET.lists()
    as_mix = {key: val[0] if val and len(val) == 1 else val for key, val in as_lists}

    # If there is no request.POST try json
    get_data = as_mix or json.loads(body)

    return get_data


def get_contract(request, request_contract):
    if isfunction(request_contract):
        request_contract_actual = request_contract(request.user)
    else:
        request_contract_actual = request_contract

    return request_contract_actual(request.data)
