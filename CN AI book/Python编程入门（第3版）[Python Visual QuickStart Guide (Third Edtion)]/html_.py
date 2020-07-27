import urllib.request

def html_():
    page = urllib.request. urlopen('http://www.baidu.org')

    html = page.read()
    print(html[:25])
