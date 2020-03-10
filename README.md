# Django Contracts
This is a lightweight (and hopefully minimally opinionated) library that 
exists to make it easier to apply Django Forms to your views. If you need
more complex capabilities than what Django Forms offers then you might want
to consider something like Django REST Framework. 

## Basic Usage
```python
from django_contracts.contracts import apply


@apply(MyFormClass, for_method='POST')
def my_view(request):
    # If you get here then the request matched your contract
    data = request.validated_data
    
    # ... do something with the data
```

You can also supply a function which returns a Django Form class to use as a 
contract. This is helpful if you need a form to be specific to a user.

```python
from django import forms
from django_contracts.contracts import apply

def create_form_for_user(user):
    class MyUserForm(forms.Form):
        # ... 
    
    return MyUserForm
    

@apply(create_form_for_user, for_method='POST')
def my_view(request):
    # ... 
```

Or if you prefer to override __init__ on the form:
```python
from django import forms
from django_contracts.contracts import apply

class MyUserForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(*args, **kwargs)
        self.user = user

@apply(lambda user: lamba data: MyUserForm(user, data))
def my_view(request)
    # ...
```