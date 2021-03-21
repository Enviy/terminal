import os
import requests
import logging

vtlog = logging.getLogger(__name__)
key = os.environ.get('VTKEY')


def getComment(h):
    if not key:
        vtlog.warn('[!] failed to load vtkey; exiting.')
        return False
    url = "https://virustotal.com/vtapi/v2/comments/get"
    query = {"apikey": key, "resource": h}
    r = requests.request("GET", url, params=query)
    if r.status_code == 200:
        r = r.json()
        return r.get('comments')
    else:
        return vtlog.warn('[!] Non-200 response: {0}'.format(r))

