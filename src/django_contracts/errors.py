from django import http


def handle_api_form_errors(form):
    """
    Automatically transforms form errors into the correct http response.

    :param form: The form with errors to handle
    :type form: django.forms.Form
    :return: The error response for the user
    :rtype: django.http.response.HttpResponse
    """
    # Most of the time we'll want to return a 400 BAD REQUEST
    response_class = http.HttpResponseBadRequest

    # But if something has a special error code we will return a more specific response
    forbidden = sniff_error_code("permissions", form.errors)
    not_found = sniff_error_code("not_found", form.errors)

    if forbidden:
        response_class = http.HttpResponseForbidden
    elif not_found:
        response_class = http.HttpResponseNotFound

    return response_class(
        content=form.errors.as_json()
    )


def sniff_error_code(error_code, form_errors):
    """
    Iterates over each error code in the error dictionary and returns True if `error_code` is found.

    :param error_code: The error_code to check for
    :type error_code: str
    :param form_errors: The error dictionary to search through
    :type form_errors: django.forms.utils.ErrorDict
    :return: True if the error code is found otherwise false
    :rtype: bool
    """
    error_values = form_errors.as_data().values()
    return any(any(error.code == error_code for error in errors) for errors in error_values)