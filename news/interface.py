import datetime
import json
import os
import time
import hashlib
import utils
import inner_server
import time

from django.conf import settings
from django.utils.crypto import constant_time_compare
from django.utils.encoding import smart_str
from django.db import transaction
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from utils import format_return, format_date_time, Validator
from decorator import validate_params
from news.models import News, Attachments
from account.models import User
from datetime import timezone, timedelta


class NewsInformation(object):
    """
    新闻资讯接口
    """
    def get_news_information(self, news_id, category, title, start_time, end_time, news_state, release_location):
        """
        筛选新闻
        """
        now_time = datetime.datetime.now()
        news_list = News.objects.filter(category=category).exclude(news_state=-1).order_by('-create_time')

        if news_id:
            news_list = news_list.filter(id=news_id)
        if title:
            news_list = news_list.filter(title=title)
        if news_state and news_state != 3:
            news_list = news_list.filter(news_state=news_state)
        if news_state == 3:
            news_list = news_list.filter(news_state=0).filter(release_time__gt=format_date_time(now_time))
        if release_location:
            news_list = news_list.filter(release_location=release_location)
        if start_time:
            news_list = news_list.filter(release_time__gte=start_time)
        if end_time:
            news_list = news_list.filter(release_time__lte=end_time)
        return news_list

    def get_web_information(self, category, release_location, news_id):
        """
        官网页面显示
        """
        now_time = datetime.datetime.now()
        news_list = News.objects.filter(news_state=0, release_time__lte=format_date_time(now_time))
        if category:
            news_list = news_list.filter(category=category)
        if release_location:
            news_list = news_list.filter(release_location=release_location)
        if news_id:
            news_list = news_list.filter(id=news_id)
        return news_list

    def news_details(self, news_id):
        """
        新闻详情
        """
        news = self.get_news_by_id(news_id)
        news.views_number += 1
        news.save()
        return news

    def add_news_information(self, user_id, category, title,  release_time, release_location=None, topping=None,
                             figure=None, explain=None, news_time=None, news_text=None, examine=None, jump_link=None,
                             banner_format=None, banner_order=None, news_file=None):
        """
        添加新闻
        """
        admin = Validator().get_user_by_id(user_id)
        news = News.objects.create(
            user=admin,
            release_location=release_location,
            title=title,
            topping=topping,
            figure=figure,
            explain=explain,
            news_time=news_time,
            release_time=release_time,
            news_text=news_text,
            examine=examine,
            news_state=1,
            category=category,
            jump_link=jump_link,
            banner_format=banner_format,
            banner_order=banner_order,
        )
        if category != 0:
            news.examine = 0
            news.save()
        if news_file:
            attachments = Attachments.objects.create(news=news, news_file=news_file)

        return news

    def modify_news_information(self, news_id, title, release_time, release_location=None, topping=None, figure=None,
                                explain=None, news_time=None, news_text=None, examine=None,  jump_link=None,
                                banner_format=None, banner_order=None, news_file=None):
        """
        修改新闻
        """
        news = NewsInformation().get_news_by_id(news_id)
        if news.news_state == 0:
            news.news_state = 1
        news.examine = examine
        news.release_location = release_location
        news.news_text = news_text
        news.news_time = news_time
        news.title = title
        news.topping = topping
        news.figure = figure
        news.explain = explain
        news.release_time = release_time
        news.banner_format = banner_format
        news.banner_order = banner_order
        news.jump_link = jump_link
        news.save()
        if news_file:
            news.attachments.news_file = news_file
            news.attachments.save()
        return news

    def submit_news_information(self, category, news_id):
        """
        提交新闻
        """
        news = News.objects.filter(category=category, news_state=1, id=news_id).first()
        if not news:
            return format_return(22201, '查询不到信息')
        if news.examine == 1:
            news.news_state = 0
            news.save()
            if news.topping != 0:
                news_1 = News.objects.filter(category=category, news_state=0, topping=news.topping).exclude(id=news.id).first()
                if news_1:
                    news_1.topping = 0
                    news_1.save()
            if news.banner_order != 0:
                news_2 = News.objects.filter(category=category, news_state=0, banner_order=news.banner_order).exclude(id=news.id).first()
                if news_2:
                    news_2.banner_order = 0
                    news_2.save()
        else:
            news.news_state = 2
            news.save()
        return news

    def examine_news_information(self, category, examine_result, news_id):
        """
        审核新闻
        """
        now_time = datetime.datetime.now()
        news = News.objects.filter(category=category, news_state=2).filter(id=news_id).first()
        if not news:
            return format_return(22201, '查询不到信息')
        if int(examine_result) == 1:
            if news.release_time > now_time:
                news.news_state = 3
            else:
                news.news_state = 0
            news.save()
            if news.topping != 0:
                news_1 = News.objects.filter(category=category, news_state=0, topping=news.topping).exclude(
                    id=news.id).first()
                if news_1:
                    news_1.topping = 0
                    news_1.save()
            if news.banner_order != 0:
                news_2 = News.objects.filter(category=category, news_state=0, banner_order=news.banner_order).exclude(
                    id=news.id).first()
                if news_2:
                    news_2.banner_order = 0
                    news_2.save()
        else:
            news.news_state = 1
            news.save()
        return news


    def get_news_by_id(self, news_id):
        """
        根据图文id查询
        """
        return News.objects.filter(id=news_id).exclude(news_state=-1).first()