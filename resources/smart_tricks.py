from requests import Session
from urllib.parse import urljoin

# Use requests module ignoring baseUrl 
# https://github.com/psf/requests/issues/2554#issuecomment-109341010
class LiveServerSession(Session):
    def __init__(self, prefix_url):
        self.prefix_url = prefix_url
        super(LiveServerSession, self).__init__()

    def request(self, method, url, *args, **kwargs):
        url = urljoin(self.prefix_url, url)
        return super(LiveServerSession, self).request(method, url, *args, **kwargs)
askfor = LiveServerSession('http://localhost:5000')

# Use dictionary as object 
# https://joelmccune.com/python-dictionary-as-object/
class DictObj:
    def __init__(self, in_dict:dict):
        assert isinstance(in_dict, dict)
        for key, val in in_dict.items():
            if isinstance(val, (list, tuple)):
               setattr(self, key, [DictObj(x) if isinstance(x, dict) else x for x in val])
            else:
               setattr(self, key, DictObj(val) if isinstance(val, dict) else val)