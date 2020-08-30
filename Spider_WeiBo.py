# coding:utf-8

from CookiesProxy_Processing import source_info
from Time_Processing import format_time
from MySQL_Control import MySQLClient
from Header import UAPool
import requests
import emoji
import time
import re


class Spider:

    def __init__(self):
        self.mysql = MySQLClient()
        self.ip, self.cookies = source_info()
        self.proxy = {self.ip.split('://')[0]: self.ip}
        self.headers = {
            'Referer': 'https://m.weibo.cn/detail/4540659497441535',
            'User-Agent': UAPool().get_header(),
            'Cookie': self.cookies
        }
        self.host_url = 'https://m.weibo.cn/comments/hotflow'
        self.reply_url = 'https://m.weibo.cn/comments/hotFlowChild'
        self.count = 0

    def run(self):
        params = {
            'id': '4540659497441535',
            'mid': '4540659497441535',
            'max_id_type': '0'
        }

        max_id = None
        max_id_type = None
        while True:
            print(max_id)
            if max_id == 0:
                print('评论全部抓取完成，程序停止')
                break

            if max_id is not None:
                params['max_id'], params['max_id_type'] = str(max_id), str(max_id_type)

            if self.count / 1000 >= 1:
                self.ip, self.cookies = source_info()
                self.headers = {
                    'Referer': 'https://m.weibo.cn/detail/4540659497441535',
                    'User-Agent': UAPool().get_header(),
                    'Cookie': self.cookies
                }
                self.count = 0
            try:
                res = requests.get(self.host_url, params=params, headers=self.headers, proxies=self.proxy, timeout=5)
                if res.status_code == 200:
                    detail = res.json()['data']
                    max_id = detail['max_id']
                    max_id_type = detail['max_id_type']
                    for row in detail['data']:
                        c_id = row['rootid']
                        reply_num = int(row['total_number'])
                        self.mysql.insert(
                            row['user']['id'],
                            row['user']['screen_name'],
                            row['user']['gender'],
                            format_time(row['created_at'])[0],
                            format_time(row['created_at'])[1],
                            self.comment_processing(row['text'])
                        )
                        self.count += 1
                        if reply_num >= 100:
                            self.reply_page(c_id)
            except Exception as e:
                print(e)
                self.ip, self.cookies = source_info()
                self.headers = {
                    'Referer': 'https://m.weibo.cn/detail/4540659497441535',
                    'User-Agent': UAPool().get_header(),
                    'Cookie': self.cookies
                }

            time.sleep(1)

    def reply_page(self, cid):
        reply_max_id = 0
        reply_id_type = 0
        while True:
            if reply_id_type == 1:
                break

            params = {
                'cid': cid,
                'max_id': str(reply_max_id),
                'max_id_type': str(reply_id_type)
            }
            self.headers['Referer'] += '?cid=%s' % cid
            try:
                response = requests.get(self.reply_url, headers=self.headers, params=params, proxies=self.proxy, timeout=5)
                if response.status_code == 200:
                    reply_max_id = response.json()['max_id']
                    reply_id_type = response.json()['max_id_type']
                    data_lst = response.json()['data']
                    for detail in data_lst:
                        self.mysql.insert(
                            detail['user']['id'],
                            detail['user']['screen_name'],
                            detail['user']['gender'],
                            format_time(detail['created_at'])[0],
                            format_time(detail['created_at'])[1],
                            self.comment_processing(detail['text'])
                        )
                        self.count += 1
            except Exception as e:
                print(e)
                self.ip, self.cookies = source_info()
                self.headers = {
                    'Referer': 'https://m.weibo.cn/detail/4540659497441535',
                    'User-Agent': UAPool().get_header(),
                    'Cookie': self.cookies
                }

            time.sleep(1)

    @staticmethod
    def comment_processing(comment):
        return emoji.demojize(re.sub('回[复復]|<a.*?</a>:| <a.*?</a>:|<a.*?</a>|<span.*?</span>', ' ', comment, re.S))\
               .strip()


if __name__ == '__main__':
    Spider().run()
