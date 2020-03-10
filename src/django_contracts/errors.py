from django import http


def handle_api_form_errors(form):
    forbidden = is_error_code_present("permissions", form.errors)
    not_found = is_error_code_present("not_found", form.errors)

    response_class = http.HttpResponseBadRequest
    if forbidden:
        response_class = http.HttpResponseForbidden
    elif not_found:
        response_class = http.HttpResponseNotFound

    return response_class(
        content=form.errors.as_json(),
        content_type='application/json',
    )


def is_error_code_present(error_code, form_errors):
    error_values = form_errors.as_data().values()
    return any(any(error.code == error_code for error in errors) for errors in error_values)
