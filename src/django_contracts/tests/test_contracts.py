from django import http, forms
from django_contracts.contracts import apply
from django.test.client import RequestFactory
import json


class MyTestForm(forms.Form):
    char = forms.CharField()


@apply(MyTestForm, for_method='POST')
def my_test_view(request):
    return http.HttpResponse(
        content=json.dumps(request.validated_data),
        status=200,
    )


def test_my_test_view_works():
    request = RequestFactory().post(
        path='/test/path/',
        data={
            'char': 'a lazy brown fox',
            'other': 'a cow jumps over the moon',
        }
    )

    response = my_test_view(request)

    response_dict = json.loads(response.content)

    assert response_dict == {
        'char': 'a lazy brown fox'
    }

    assert response.status_code == 200


def test_my_test_view_returns_errors():
    request = RequestFactory().post(
        path='/test/path/',
        data={
            'char': '',
            'other': 'a cow jumps over the moon',
        }
    )

    response = my_test_view(request)

    response_dict = json.loads(response.content)

    assert response_dict == {
        'char': [
            {
                'code': 'required',
                'message': 'This field is required.',
            },
        ],
    }

    assert response.status_code == 400


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


@apply(MyAdvancedForm, for_method='POST')
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


@apply(MyTestForm, for_method='POST')
def basic_view(request):
    import pdb
    pdb.set_trace()
    return http.HttpResponse(
        content=json.dumps(request.validated_data),
        status=200,
    )


def test_bad_encoding_error():
    request = RequestFactory().post(
        path='/test/path/',
        body='some other formatting',
        encoding='application/json',
    )

    response = my_advanced_view(request)
    response_dict = json.loads(response.content)

    assert response_dict == {
        '__all__': [
            (
                'Invalid POST data. The supported MIME types for this endpoint are: '
                '[multipart/form-data, application/json]'
            ),
            'Expecting value: line 1 column 1 (char 0)',
        ],
    }
