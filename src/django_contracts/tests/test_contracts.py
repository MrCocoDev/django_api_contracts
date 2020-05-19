import json

from django import http, forms
from django.test.client import RequestFactory

from django_contracts.contracts import apply


class MyTestForm(forms.Form):
    char = forms.CharField()


def basic_view(request):
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

    response = apply(MyTestForm, for_method='POST')(basic_view)(request)

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

    response = apply(MyTestForm, for_method='POST')(basic_view)(request)

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


def test_bad_encoding_error():
    request = RequestFactory().post(
        path='/test/path/',
        body='some other formatting',
        encoding='application/json',
    )

    response = apply(MyTestForm, for_method='POST')(basic_view)(request)
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

    assert response.status_code == 400
