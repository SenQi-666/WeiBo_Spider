import requests


def source_info():
    lst = ['http://个人代理池地址，不方便透露/random', 'http://0.0.0.0:5000/weibo/random']
    for url in lst:
        response = requests.get(url)
        yield response.text
