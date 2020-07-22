import hashlib
import uuid


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
    discovery_info = {
        'specifications': {},
        'resource_id': None,
    }

    if (description := view.contracts.get('description')):
        discovery_info['description'] = description.strip()

    if (resource_id := view.contracts.get('resource_id')):
        discovery_info['resource_id'] = resource_id
    else:
        m = hashlib.md5()
        m.update(view.__name__.encode('utf-8'))
        new_uuid = uuid.UUID(m.hexdigest())
        discovery_info['resource_id'] = str(new_uuid)

    try:
        discovery_info['specifications']['request'] = {
            key: as_json(value()) for key, value in view.contracts['request'].items()
        }
    except AttributeError:
        pass

    try:
        discovery_info['specifications']['response'] = {
            key: as_json(value()) for key, value in view.contracts['response'].items()
        }
    except AttributeError:
        pass

    return discovery_info
