import urllib
import urllib2

import BeautifulSoup


class Robot(object):
    @classmethod
    def start(cls, url, postdata=None):
        headers = { 'User-Agent' : 'Mozilla/5.0' }
        req = urllib2.Request(url, postdata, headers)
        data = urllib2.urlopen(req).read()
        return cls(url, BeautifulSoup.BeautifulSoup(data))
    
    def __init__(self, url, html):
        self.url = url
        self.html = html
    
    @property
    def baseurl(self):
        if '?' in self.url:
            return self.url[:self.url.index('?')]
        else:
            return self.url
    
    def get_new_url(self, options):
        return self.baseurl + '?' + urllib.urlencode(options)
