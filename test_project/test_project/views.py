from django import forms, http
from django_contracts.contracts import apply_contract, description, resource_id


class MyForm(forms.Form):
    char = forms.CharField(min_length=10, max_length=99, strip=True, empty_value='something', required=True)
    num = forms.IntegerField(min_value=-99, max_value=100, required=True, initial=100, )


@resource_id("http_basic_view")
@description(use_view_docstring=True)
@apply_contract(
    request_contracts={'GET': MyForm, 'POST': MyForm},
    response_contracts={'GET': MyForm, 'POST': MyForm},
    pass_in_user=True,
)
def basic_view(request):
    """
    This is my function's docstring being automatically used as the public docstring.
    """
    return http.HttpResponse(
        content='Hello World',
        status=200,
    )
