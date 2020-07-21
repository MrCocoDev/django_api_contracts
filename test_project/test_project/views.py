from django import forms, http
from django_contracts.contracts import apply_contract


class MyForm(forms.Form):
    char = forms.CharField(min_length=10, max_length=99, strip=True, empty_value='something', required=True)
    num = forms.IntegerField(min_value=-99, max_value=100, required=True, initial=100, )


@apply_contract(
    request_contracts={'GET': MyForm, 'POST': MyForm},
    response_contracts={'GET': MyForm, 'POST': MyForm},
    pass_in_user=True,
)
def basic_view(request):
    return http.HttpResponse(
        content='Hello World',
        status=200,
    )
