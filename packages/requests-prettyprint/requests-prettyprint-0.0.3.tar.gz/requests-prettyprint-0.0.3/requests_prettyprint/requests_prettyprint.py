import json

def _prettyprint(res):
    req = res.request
    print('\n{}\n{}\n\n{}\n\n{}\n'.format(
        '-----------Request----------->',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body))
    text = res.text
    try:
        text = json.dumps(json.loads(text), sort_keys=True, indent=4)
    except ValueError:
        pass
    print('\n{}\n{}\n{}\n\n{}\n\n{}\n'.format(
        '<----------Response-----------',
        'Status code: ' + str(res.status_code),
        'Elapsed time (secs): ' + str(res.elapsed.total_seconds()),
        '\n'.join('{}: {}'.format(k, v) for k, v in res.headers.items()),
        text))

def prettyprint(res):
    for r in res.history:
        _prettyprint(r)
    _prettyprint(res)

if __name__ == '__main__':
    import requests
    r = requests.get('http://google.com')
    prettyprint(r)
