
import urllib
import json

def short(url, short_url='http://s.prod.uci.cu'):
    try:
        response = urllib.urlopen(
            short_url + '/?' + urllib.urlencode({'url': url}))
    except IOError:
        return None
    if response.getcode() == 200:
        data = json.loads(response.read())
        if 'url' in data:
            return short_url + data['url']
    raise ValueError

if __name__ == '__main__':
    print short('http://comunidades.uci.cu')
