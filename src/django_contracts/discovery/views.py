import json
import re
from . import get_application_discovery_document


def http_discovery_view(request, url):
    discovery_document = json.dumps(get_application_discovery_document())

    payload = {}

    if not url:
        payload = json.dumps(discovery_document)

    else:
        for url_regex in discovery_document.keys():
            if re.match(url_regex, url):
                payload = {
                    url_regex: discovery_document[url_regex],
                }

    return payload