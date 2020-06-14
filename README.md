# Django Contracts
This is a lightweight (and hopefully minimally opinionated) library that 
exists to make it easier to apply Django Forms to your views. If you need
more complex capabilities than what Django Forms offers then you might want
to consider something like Django REST Framework. 

## Basic Usage
```python
from django_contracts.contracts import apply_contract


@apply_contract(request_contracts={'POST': MyRequestForm}, response_contracts={'POST': MyResponseForm})
def my_view(request):
    # If you get here then the request matched your contract
    data = request.validated_data
    
    # ... do something with the data
```

You can also supply a function which returns a Django Form class to use as a 
contract. This is helpful if you need a form to be specific to a user.

```python
from django import forms
from django_contracts.contracts import request_contract

def create_form_for_user(user, data):
    class MyUserForm(forms.Form):
        # ... 
        if user_can_do_thing:
            my_field = ...
    
    return MyUserForm(data)
    

@apply_contract(request_contracts={'POST': create_form_for_user}, pass_in_user=True)
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

@apply_contract(request_contracts={'POST': create_form_for_user}, pass_in_user=True)
def my_view(request)
    # ...
```

Using forms that take a `User` can be useful for filtering choice options.