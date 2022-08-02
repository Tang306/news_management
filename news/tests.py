import json
import jwt
import datetime
from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from account.interface import UserBase
from datetime import datetime
import time


class NewsTestCase(TestCase):
    def setUp(self):
        self.nickname = '管理员'
        self.username = '13888888888'
        self.password = 'test_123456'
        self.app_id = 'app_id'
        self.client = Client(HTTP_APPID=self.app_id)

        admin = UserBase().admin_register(nickname=self.nickname, username=self.username, password=self.password)

    def test_add_news(self):
        result = self.client.post(
            '/account/api/login', {
                'username': self.username, 'password': self.password
            }
        ).json()
        token = result['data']['token']

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/add_news', {
                'category': 0, 'release_location': 1, 'title': '标题1', 'topping': 1,
                'news_time': '2013-10-31 18:23:29.000227',
                'news_text': '新闻正文', 'examine': 0, 'release_time': '2013-10-31 18:23:29.000227',
            }
        ).json()
        print(result)
        self.assertEqual(result['data']['category'], '0')
        self.assertEqual(result['data']['news_state'], 1)  # 发布新闻资讯

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/add_news', {
                'category': 1, 'release_location': 1, 'title': '标题2', 'figure': '1',
                'release_time': '2013-10-31 18:23:29.000227',
            }
        ).json()
        print(result)
        self.assertEqual(result['data']['category'], '1')
        self.assertEqual(result['data']['news_state'], 1)  # 发布员工活动

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/add_news', {
                'category': 2, 'title': '标题3', 'banner_format': 0, 'figure': '1',
                'release_time': '2013-10-31 18:23:29.000227', 'banner_order': 2,
            }
        ).json()
        print(result)
        self.assertEqual(result['data']['category'], '2')
        self.assertEqual(result['data']['news_state'], 1)  # 发布banner

    def test_get_news(self):
        result = self.client.post(
            '/account/api/login', {
                'username': self.username, 'password': self.password
            }
        ).json()
        token = result['data']['token']

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/add_news', {
                'category': 0, 'release_location': 1, 'title': '标题', 'topping': 1,
                'news_time': '2013-10-31 18:23:29.000227', 'news_text': '新闻正文', 'examine': 0,
                'release_time': '2013-10-31 18:23:29.000227',
            }
        ).json()

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/add_news', {
                'category': 0, 'release_location': 1, 'title': '标题11', 'topping': 1,
                'news_time': '2013-10-31 18:23:29.000227', 'news_text': '新闻正文', 'examine': 0,
                'release_time': '2013-10-31 18:23:29.000227',
            }
        ).json()

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/add_news', {
                'category': 0, 'release_location': 1, 'title': '标题22', 'topping': 1,
                'news_time': '2013-10-31 18:23:29.000227', 'news_text': '新闻正文', 'examine': 0,
                'release_time': '2013-10-31 18:23:29.000227',
            }
        ).json()

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/news_list', {
                'category': 0, 'title': '标题',
            }
        ).json()
        self.assertEqual(result['code'], 0)

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/news_list', {
                'category': 0, 'title': '标题1',
            }
        ).json()
        self.assertEqual(result['code'], 22201)

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/news_list', {
                'category': 0,
            }
        ).json()
        print(result)

    def test_get_news_info(self):
        result = self.client.post(
            '/account/api/login', {
                'username': self.username, 'password': self.password
            }
        ).json()
        token = result['data']['token']

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/add_news', {
                'category': 0, 'release_location': 1, 'title': '标题', 'topping': 1, 'news_time': '2013-10-31 18:23:29.000227',
                'news_text': '新闻正文11', 'examine': 0, 'release_time': '2013-10-31 18:23:29.000227',
            }
        ).json()

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/get_news_info', {
                'news_id': 1,
            }
        ).json()
        print(result)
        self.assertEqual(result['data']['news_text'], '新闻正文11')

    def test_post_news(self):
        result = self.client.post(
            '/account/api/login', {
                'username': self.username, 'password': self.password
            }
        ).json()
        token = result['data']['token']

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/add_news', {
                'category': 0, 'release_location': 1, 'title': '标题1', 'topping': 1,
                'news_time': '2013-10-31 18:23:29.000227', 'news_text': '新闻正文', 'examine': 1,
                'release_time': '2013-10-31 18:23:29.000227',
            }
        ).json()
        print(result)
        self.assertEqual(result['data']['title'], '标题1')

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/post_news', {
                'category': 0, 'release_location': 1, 'news_id': 1, 'title': '标题11', 'topping': 1,
                'news_time': '2013-10-31 18:23:29.000227', 'news_text': '新闻正文', 'examine': 0,
                'release_time': '2013-10-31 18:23:29.000227',
            }
        ).json()
        print(result)
        self.assertEqual(result['data']['title'], '标题11')  # 修改新闻资讯

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/add_news', {
                'category': 1, 'release_location': 1, 'title': '标题2', 'figure': '1',
                'release_time': '2013-10-31 18:23:29.000227',
            }
        ).json()
        print(result)
        self.assertEqual(result['data']['title'], '标题2')

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/post_news', {
                'category': 1, 'news_id': 2, 'release_location': 1, 'title': '标题22', 'figure': '1',
                'release_time': '2013-10-31 18:23:29.000227',
            }
        ).json()
        print(result)
        self.assertEqual(result['data']['title'], '标题22')  # 修改员工活动

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/add_news', {
                'category': 2, 'title': '标题3', 'banner_format': 0, 'figure': '1',
                'release_time': '2013-10-31 18:23:29.000227', 'banner_order': 2,
            }
        ).json()
        print(result)
        self.assertEqual(result['data']['title'], '标题3')

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/post_news', {
                'category': '2', 'news_id': 3, 'title': '标题33', 'banner_format': 0, 'figure': '1',
                'release_time': '2013-10-31 18:23:29.000227', 'banner_order': 2,
            }
        ).json()
        print(result)
        self.assertEqual(result['data']['title'], '标题33')  # 修改banner

    def test_del_news(self):
        result = self.client.post(
            '/account/api/login', {
                'username': self.username, 'password': self.password
            }
        ).json()
        token = result['data']['token']

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/add_news', {
                'category': 0, 'release_location': 1, 'title': '标题', 'topping': 1, 'news_time': '2013-10-31 18:23:29.000227',
                'news_text': '新闻正文', 'examine': 0, 'release_time': '2013-10-31 18:23:29.000227',
            }
        ).json()

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/del_news', {
                'news_id': 1
            }
        ).json()
        print(result)
        self.assertEqual(result['data']['news_state'], -1)

    def test_sub_news(self):
        result = self.client.post(
            '/account/api/login', {
                'username': self.username, 'password': self.password
            }
        ).json()
        token = result['data']['token']

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/add_news', {
                'category': 0, 'release_location': 1, 'title': '标题1', 'topping': 1, 'news_time': '2013-10-31 18:23:29.000227',
                'news_text': '新闻正文1', 'examine': 0, 'release_time': '2013-10-31 18:23:29.000227',
            }
        ).json()

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/submit_news', {
                'category': 0, 'news_id': 1
            }
        ).json()
        self.assertEqual(result['data']['news_state'], 2)

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/add_news', {
                'category': 0, 'release_location': 1, 'title': '标题2', 'topping': 1,
                'news_time': '2013-10-31 18:23:29.000227',
                'news_text': '新闻正文2', 'examine': 1, 'release_time': '2013-10-31 18:23:29.000227',
            }
        ).json()

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/submit_news', {
                'category': 0, 'news_id': 2
            }
        ).json()
        print(result)
        self.assertEqual(result['data']['news_state'], 0)

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/add_news', {
                'category': 0, 'release_location': 1, 'title': '标题3', 'topping': 1,
                'news_time': '2013-10-31 18:23:29.000227',
                'news_text': '新闻正文3', 'examine': 1, 'release_time': '2013-10-31 18:23:29.000227',
            }
        ).json()

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/submit_news', {
                'category': 0, 'news_id': 3
            }
        ).json()
        print(result)
        self.assertEqual(result['data']['topping'], 1)

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/news_list', {
                'category': 0, 'news_id': 2,
            }
        ).json()
        print(result)
        for item in result['data']['objs']:
            self.assertEqual(item['topping'], 0)

    def test_examine_news(self):
        result = self.client.post(
            '/account/api/login', {
                'username': self.username, 'password': self.password
            }
        ).json()
        token = result['data']['token']

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/add_news', {
                'category': 0, 'release_location': 1, 'title': '标题1', 'topping': 1,
                'news_time': '2013-10-31 18:23:29.000227',
                'news_text': '新闻正文1', 'examine': 0, 'release_time': '2013-10-31 18:23:29.000227',
            }
        ).json()

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/add_news', {
                'category': 0, 'release_location': 1, 'title': '标题2', 'topping': 2,
                'news_time': '2013-10-31 18:23:29.000227',
                'news_text': '新闻正文2', 'examine': 0, 'release_time': '2023-10-31 18:23:29.000227',
            }
        ).json()

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/submit_news', {
                'category': 0, 'news_id': 1
            }
        ).json()
        self.assertEqual(result['data']['news_state'], 2)

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/submit_news', {
                'category': 0, 'news_id': 2
            }
        ).json()
        self.assertEqual(result['data']['news_state'], 2)

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/examine_news', {
                'category': 0, 'examine_result': 0, 'news_id': 1
            }
        ).json()
        self.assertEqual(result['data']['news_state'], 1)

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/examine_news', {
                'category': 0, 'examine_result': 1, 'news_id': 2
            }
        ).json()
        print(result['data']['news_state'])
        self.assertEqual(result['data']['news_state'], 3)

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/submit_news', {
                'category': 0, 'news_id': 1
            }
        ).json()
        self.assertEqual(result['data']['news_state'], 2)

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/examine_news', {
                'category': 0, 'examine_result': 1, 'news_id': 1
            }
        ).json()
        self.assertEqual(result['data']['news_state'], 0)

    def test_web_news(self):
        result = self.client.post(
            '/account/api/login', {
                'username': self.username, 'password': self.password
            }
        ).json()
        token = result['data']['token']

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/add_news', {
                'category': 0, 'release_location': 1, 'title': '标题1', 'topping': 1,
                'news_time': '2013-10-31 18:23:29.000227',
                'news_text': '新闻正文1', 'examine': 1, 'release_time': '2013-10-31 18:23:29.000227',
            }
        ).json()

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/add_news', {
                'category': 0, 'release_location': 1, 'title': '标题2', 'topping': 1,
                'news_time': '2013-10-31 18:23:29.000227',
                'news_text': '新闻正文1', 'examine': 1, 'release_time': '2023-10-31 18:23:29.000227',
            }
        ).json()

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/submit_news', {
                'category': 0, 'news_id': 1
            }
        ).json()

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/news_list', {
                'category': 0, 'news_id': 1,
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 0)

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/web_list', {
                'category': 0, 'news_id': 1
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 0)

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/submit_news', {
                'category': 0, 'news_id': 2
            }
        ).json()

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/news_list', {
                'category': 0, 'news_id': 2,
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 0)

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/news/api/web_list', {
                'news_id': 2
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 22201)