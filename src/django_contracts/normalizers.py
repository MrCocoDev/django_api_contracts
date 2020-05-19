import json
from functools import wraps

from django import http, forms


class ErrorForm(forms.Form):

    reason = forms.CharField()

    def clean(self):
        raise forms.ValidationError(
            [
                forms.ValidationError(
                    message=(
                        "Invalid POST data. "
                        "The supported MIME types for this endpoint are: "
                        "[multipart/form-data, application/json]"
                    ),
                    code="invalid"
                ),
                forms.ValidationError(
                    message=self.data['reason'],
                    code="invalid"
                ),
            ],
        )


def normalize_view_data(func, request_type):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            request.data = normalize_request_data(request, request_type)
        except json.JSONDecodeError as e:
            errors = ErrorForm({'reason': str(e)})
            errors.is_valid()
            return http.HttpResponseBadRequest(
                content=json.dumps(errors.errors),
                content_type="application/json"
            )

        return func(request, *args, **kwargs)

    return wrapper


def normalize_request_data(request, request_type):
    body = request.body or '{}'

    # request.POST.dict() only takes a single value from array inputs so we use `lists` and transform
    # singular values back
    as_lists = getattr(request, request_type).lists()
    as_mix = {key: val[0] if val and len(val) == 1 else val for key, val in as_lists}

    # If there is no request.POST try json
    post_data = as_mix or json.loads(body)

    return post_data
