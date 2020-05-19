import json

from django import http, forms
from django.test.client import RequestFactory

from django_contracts.contracts import apply
from unittest import mock


class MyUserForm(forms.Form):
    char = forms.CharField()

    def __init__(self, data, user, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        self.user = user
        if self.user.username == 'valid':
            self.fields['hidden'] = forms.CharField()


@apply(MyUserForm, for_method='POST', pass_in_user=True, )
def basic_view(request):
    return http.HttpResponse(
        content=json.dumps(request.validated_data),
        status=200,
    )


def test_user_a_cannot_use_hidden_field():
    user = mock.Mock(username='user_a')

    request = RequestFactory().post(
        path='/test/path/',
        data={
            'char': 'I am allowed to use this.',
            'hidden': 'Arrr! I will use any API I want!',
        }
    )

    request.user = user

    response = basic_view(request)

    response_dict = json.loads(response.content)

    assert response_dict == {
        'char': 'I am allowed to use this.',
    }

    assert response.status_code == 200


def test_user_a_cannot_use_hidden_field():
    user = mock.Mock(username='valid')

    request = RequestFactory().post(
        path='/test/path/',
        data={
            'char': 'I am allowed to use this.',
            'hidden': 'Huzzah! Great privilege.',
        }
    )

    request.user = user

    response = basic_view(request)

    response_dict = json.loads(response.content)

    assert response_dict == {
        'char': 'I am allowed to use this.',
        'hidden': 'Huzzah! Great privilege.',
    }

    assert response.status_code == 200