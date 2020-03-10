from django import http


def handle_api_form_errors(form):
    response_status = 400  # Default to 400
    default_mapping = [
        ('unauthorized', 403),
        ('not_found', 404),
        ('missing', 404),
        ('invalid', 400),
    ]
    try:
        mapping = form.Meta.code_mapping
        full_mapping = mapping + default_mapping
    except AttributeError:
        full_mapping = default_mapping

    for code, status in full_mapping:
        if is_error_code_present(code, form.errors):
            response_status = status

    return http.HttpResponse(
        content_type='application/json',
        content=form.errors.as_json(),
        status=response_status,
    )


def is_error_code_present(error_code, form_errors):
    error_values = form_errors.as_data().values()
    return any(any(error.code == error_code for error in errors) for errors in error_values)
