
import urllib.request
import json


def get_object(url):
    """
    Utility to obtain a python object from the api_path you provide.
    """
    stream = urllib.request.urlopen(url)
    bytes = stream.read()
    encoding = stream.info().get_content_charset('utf-8')
    return json.loads(bytes.decode(encoding))
