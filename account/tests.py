from django.test import TestCase
from django.test.client import Client
from account.interface import UserBase


class AccountTestCase(TestCase):
    def setUp(self):
        self.nickname = '管理员'
        self.username = '13888888888'
        self.password = 'test_123456'
        self.app_id = 'app_id'
        self.client = Client(HTTP_APPID=self.app_id)

        admin = UserBase().admin_register(nickname=self.nickname, username=self.username, password=self.password)

    def test_register(self):
        # result = self.client.post(
        #     '/account/api/register_supper', {
        #         'nickname': self.nickname, 'username': self.username, 'password': self.password
        #     }
        # ).json()

        result = self.client.post(
            '/account/api/login', {
                'username': self.username, 'password': self.password
            }
        ).json()
        token = result['data']['token']

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/account/api/register', {
                'nickname': '小王123', 'username': 14888888888, 'password': 'test_1234', 'state': 2
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 0)

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/account/api/register', {
                'nickname': '小王123', 'username': 148, 'password': 'test_1234', 'state': 2
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 11000)

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/account/api/register', {
                'nickname': '小王123', 'username': '142w', 'password': 'test_1234', 'state': 2
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 11001)

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/account/api/register', {
                'nickname': '小王123', 'username': 15888888888, 'password': 'te1', 'state': 2
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 11002)

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/account/api/register', {
                'nickname': '小王123', 'username': 14888888888, 'password': 'test_1234', 'state': 2
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 11005)

    def test_login(self):
        result = self.client.post(
            '/account/api/login', {
                'username': self.username, 'password': self.password
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 0)

        result = self.client.post(
            '/account/api/login', {
                'username': 14888888888, 'password': self.password
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 11004)

        result = self.client.post(
            '/account/api/login', {
                'username': self.username, 'password': '21w2'
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 11002)

        result = self.client.post(
            '/account/api/login', {
                'username': self.username, 'password': 'test_1111'
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 11003)

    def test_change_pwd(self):
        result = self.client.post(
            '/account/api/login', {
                'username': self.username, 'password': self.password
            }
        ).json()
        token = result['data']['token']

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/account/api/change', {
                'old_password': self.password, 'new_password': 'test_9876'
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 0)

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/account/api/change', {
                'old_password': self.password, 'new_password': 'test_1212'
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 11003)

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/account/api/change', {
                'old_password': 'test_9876', 'new_password': 'te1'
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 11002)

    def test_initial_pwd(self):
        result = self.client.post(
            '/account/api/login', {
                'username': self.username, 'password': self.password
            }
        ).json()
        token = result['data']['token']

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/account/api/register', {
                'nickname': '小王123', 'username': 14888888888, 'password': 'test_1234', 'state': 2
            }
        ).json()

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/account/api/reset', {
                'user_id': 2
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 0)

        result = self.client.post(
            '/account/api/login', {
                'username': 14888888888, 'password': 'test_8888'
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 0)

        result = self.client.post(
            '/account/api/login', {
                'username': 14888888888, 'password': 'test_1234'
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 11003)

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/account/api/reset', {
                'user_id': 3
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 11004)

    def test_decorator(self):
        result = self.client.post(
            '/account/api/login', {
                'username': self.username, 'password': self.password
            }
        ).json()
        token = result['data']['token']

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/account/api/register', {
                'nickname': '小王123', 'username': 14888888888, 'password': 'test_1234', 'state': 2
            }
        ).json()

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/account/api/register', {
                'nickname': '小李123', 'username': 15888888888, 'password': 'test_4321', 'state': 2
            }
        ).json()

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/account/api/reset', {
                'user_id': 3
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 0)

        result = Client(HTTP_AUTHORIZATION='42wd').post(
            '/account/api/reset', {
                'user_id': 3
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 11009)

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/account/api/reset', {
                'user_id': 4
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 11004)

        result = Client(HTTP_AUTHORIZATION='').post(
            '/account/api/reset', {
                'user_id': 3
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 11006)

        # print("start:%s" % time.ctime())
        # time.sleep(70)
        # print("end:%s" % time.ctime())
        #
        # result = Client(HTTP_AUTHORIZATION=token).post(
        #     '/account/api/reset', {
        #         'user_id': 3
        #     }
        # ).json()
        # print(result)
        # self.assertEqual(result['code'], 11008)

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/account/api/login', {
                'username': 14888888888, 'password': 'test_1234'
            }
        ).json()
        token1 = result['data']['token']

        result = Client(HTTP_AUTHORIZATION=token1).post(
            '/account/api/reset', {
                'user_id': 3
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 11007)

    def test_del_user(self):
        result = self.client.post(
            '/account/api/login', {
                'username': self.username, 'password': self.password
            }
        ).json()
        token = result['data']['token']

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/account/api/register', {
                'nickname': '小王123', 'username': 14888888888, 'password': 'test_1234', 'state': 2
            }
        ).json()

        result = self.client.post(
            '/account/api/login', {
                'username': 14888888888, 'password': 'test_1234'
            }
        ).json()

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/account/api/user_delete', {
                'user_id': 2
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 0)

        result = self.client.post(
            '/account/api/login', {
                'username': 14888888888, 'password': 'test_1234'
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 11004)

    def test_edit_user(self):
        result = self.client.post(
            '/account/api/login', {
                'username': self.username, 'password': self.password
            }
        ).json()
        token = result['data']['token']

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/account/api/register', {
                'nickname': '小王123', 'username': 14888888888, 'password': 'test_1234', 'state': 2
            }
        ).json()

        result = self.client.post(
            '/account/api/login', {
                'username': 14888888888, 'password': 'test_1234'
            }
        ).json()

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/account/api/user_edit', {
                'user_id': 3, 'nickname': '小明222', 'username': 15888888888, 'password': 'test_4321', 'state': 3
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 11004)

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/account/api/user_edit', {
                'user_id': 2, 'nickname': '小明222', 'username': 15888888888, 'password': '5st', 'state': 3
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 11002)

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/account/api/user_edit', {
                'user_id': 2, 'nickname': '小明222', 'username': 15888888888, 'password': 'test_4321', 'state': 3
            }
        ).json()
        print(result)
        self.assertEqual(result['data']['state'], '3')

    def test_get_user(self):
        result = self.client.post(
            '/account/api/login', {
                'username': self.username, 'password': self.password
            }
        ).json()
        token = result['data']['token']

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/account/api/register', {
                'nickname': '小王123', 'username': 14888888888, 'password': 'test_1234', 'state': 2
            }
        ).json()

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/account/api/register', {
                'nickname': '小赵123', 'username': 15888888888, 'password': 'test_1234', 'state': 2
            }
        ).json()

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/account/api/register', {
                'nickname': '小钱123', 'username': 16888888888, 'password': 'test_1234', 'state': 3
            }
        ).json()

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/account/api/register', {
                'nickname': '小孙123', 'username': 17888888888, 'password': 'test_1234', 'state': -1
            }
        ).json()

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/account/api/register', {
                'nickname': '小李123', 'username': 18888888888, 'password': 'test_1234', 'state': 3
            }
        ).json()

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/account/api/user_list', {
                'nickname': '小王123',
            }
        ).json()
        print(result)
        self.assertEqual(result['code'], 0)

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/account/api/user_list', {
                'state': 2,  # 启用用户
            }
        ).json()
        print(result)
        for item in result['data']['objs']:
            self.assertNotEqual(item['state'], -1)

        result = Client(HTTP_AUTHORIZATION=token).post(
            '/account/api/user_list', {
                'state': -1,  # 禁用用户
            }
        ).json()
        print(result)
        for item in result['data']['objs']:
            self.assertEqual(item['state'], -1)


