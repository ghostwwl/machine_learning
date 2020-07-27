import urllib.parse
import urllib.request

url = "http://www.baidu.com"
values = {"rls":"ig"}
data = urllib.parse.urlencode(values)

theurl = url+"?"+data

req = urllib.request.Request(theurl)
res = urllib.request.urlopen(req)
page = res.read()
