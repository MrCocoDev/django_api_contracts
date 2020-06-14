
from django import forms, http
from django_contracts.discovery.primitives import as_json, view_to_json

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


def test_json_serializing_form_definition():
    json_repr = as_json(MyForm())

    assert json_repr == {
        'char': {
            'default': None,
            'required': True,
            'type': 'text',
            'maxlength': '99',
            'minlength': '10',
        },
        'num': {
            'default': 100,
            'required': True,
            'type': 'number',
            'min': -99,
            'max': 100,
        },
    }


def test_get_discovery_documentation_from_view_request_contract():
    json_repr = as_json(basic_view.contracts['request']['POST']())

    assert json_repr == {
        'char': {
            'default': None,
            'required': True,
            'type': 'text',
            'maxlength': '99',
            'minlength': '10',
        },
        'num': {
            'default': 100,
            'required': True,
            'type': 'number',
            'min': -99,
            'max': 100,
        },
    }


def test_get_discovery_documentation_from_view():
    json_repr = view_to_json(basic_view)

    assert json_repr == {
        'request': {
            'GET': {
                'char': {
                    'default': None,
                    'required': True,
                    'type': 'text',
                    'maxlength': '99',
                    'minlength': '10',
                },
                'num': {
                    'default': 100,
                    'required': True,
                    'type': 'number',
                    'min': -99,
                    'max': 100,
                },
            },
            'POST': {
                'char': {
                    'default': None,
                    'required': True,
                    'type': 'text',
                    'maxlength': '99',
                    'minlength': '10',
                },
                'num': {
                    'default': 100,
                    'required': True,
                    'type': 'number',
                    'min': -99,
                    'max': 100,
                },
            },
        },
        'response': {
            'GET': {
                'char': {
                    'default': None,
                    'required': True,
                    'type': 'text',
                    'maxlength': '99',
                    'minlength': '10',
                },
                'num': {
                    'default': 100,
                    'required': True,
                    'type': 'number',
                    'min': -99,
                    'max': 100,
                },
            },
            'POST': {
                'char': {
                    'default': None,
                    'required': True,
                    'type': 'text',
                    'maxlength': '99',
                    'minlength': '10',
                },
                'num': {
                    'default': 100,
                    'required': True,
                    'type': 'number',
                    'min': -99,
                    'max': 100,
                },
            },
        }
    }
