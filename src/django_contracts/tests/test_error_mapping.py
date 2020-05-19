import json

from django import http, forms
from django.test.client import RequestFactory

from django_contracts.contracts import apply


class MyAdvancedForm(forms.Form):
    char = forms.CharField()

    def clean_char(self):
        value = self.cleaned_data['char']

        if value == 'unauthorized choice':
            raise forms.ValidationError('Intruder!', code='unauthorized')

        elif value == 'missing choice':
            raise forms.ValidationError('404 not found.', code='not_found')

        elif value == 'custom choice':
            raise forms.ValidationError('Conflict!', code='custom')

        else:
            raise forms.ValidationError('Something else went wrong', code='invalid')

    class Meta:
        code_mapping = [
            ('custom', 409),
        ]


@apply(MyAdvancedForm, for_method='POST', pass_in_user=False)
def my_advanced_view(request):
    return http.HttpResponse(
        content=json.dumps(request.validated_data),
        status=200,
    )


def test_my_advanced_view_returns_errors_unauthorized():
    request = RequestFactory().post(
        path='/test/path/',
        data={
            'char': 'unauthorized choice',
        }
    )

    response = my_advanced_view(request)

    response_dict = json.loads(response.content)

    assert response_dict == {
        'char': [
            {
                'code': 'unauthorized',
                'message': 'Intruder!',
            },
        ],
    }

    assert response.status_code == 403


def test_my_advanced_view_returns_errors_not_found():
    request = RequestFactory().post(
        path='/test/path/',
        data={
            'char': 'missing choice',
        }
    )

    response = my_advanced_view(request)

    response_dict = json.loads(response.content)

    assert response_dict == {
        'char': [
            {
                'code': 'not_found',
                'message': '404 not found.',
            },
        ],
    }

    assert response.status_code == 404


def test_my_advanced_view_returns_errors_invalid():
    request = RequestFactory().post(
        path='/test/path/',
        data={
            'char': 'invalid choice',
        }
    )

    response = my_advanced_view(request)

    response_dict = json.loads(response.content)

    assert response_dict == {
        'char': [
            {
                'code': 'invalid',
                'message': 'Something else went wrong',
            },
        ],
    }

    assert response.status_code == 400


def test_my_advanced_view_returns_errors_custom():
    request = RequestFactory().post(
        path='/test/path/',
        data={
            'char': 'custom choice',
        }
    )

    response = my_advanced_view(request)

    response_dict = json.loads(response.content)

    assert response_dict == {
        'char': [
            {
                'code': 'custom',
                'message': 'Conflict!',
            },
        ],
    }

    assert response.status_code == 409
