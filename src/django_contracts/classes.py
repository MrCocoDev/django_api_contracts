from django import forms


class Contract(forms.Form):

    def __init__(self, data, user, *args, **kwargs):
        self.user = user
        super().__init__(data, *args, **kwargs, )
