from django.urls import get_resolver

from .primitives import view_to_json


def get_application_discovery_document():
    serializing_iterator = (
        (view_to_json(vf), url_info)
        for vf, url_info in get_resolver().reverse_dict.items() if callable(vf)
    )

    make_into_list_of_dictionaries = [
        {
            'url': x[1][1],
            'specifications': x[0],
        }
        for x in serializing_iterator
        if x[0]
    ]

    return make_into_list_of_dictionaries
