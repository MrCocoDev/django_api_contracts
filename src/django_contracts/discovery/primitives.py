

def as_json(form):
    return {field_name: serialize_field(field) for field_name, field in form.fields.items()}


def serialize_field(field):
    return {
        'default': field.initial,
        'required': field.required,
        'type': field.widget.input_type,
        **field.widget_attrs(field.widget),
    }


def view_to_json(view):
    discovery_info = {}

    try:
        discovery_info['request'] = {key: as_json(value()) for key, value in view.contracts['request'].items()}
    except AttributeError:
        pass

    try:
        discovery_info['response'] = {key: as_json(value()) for key, value in view.contracts['response'].items()}
    except AttributeError:
        pass

    return discovery_info
