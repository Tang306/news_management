from django.db import models
from account.models import User


class News(models.Model):
    """
    新闻信息类
    """
    news_state_choices = ((-1, '删除'), (0, '已发布'), (1, '未发布'), (2, '审核中'))
    category_choices = ((0, '新闻资讯'), (1, '员工风采'), (2, 'banner发布'),)
    examine_choices = ((0, '是'), (1, '否'))
    topping_choices = ((1, '首页第一位'), (2, '首页第二位'), (0, '否'))
    banner_format_choices = ((0, '图片'), (1, '视频'))
    banner_order_choices = ((0, '下架'), (1, '轮播图第一位'), (2, '轮播图第一位'), (3, '轮播图第三位'), (4, '轮播图第四位'))
    release_location_choices = ((1, '关于我们-新闻资讯'), (2, '专项行动-学习文件'), (3, '专项行动-相关资讯'))
    examine_result_choices = ((0, '审核失败'), (1, '审核成功'))

    title = models.CharField('标题', max_length=128)
    category = models.IntegerField('新闻信息类别', default=0, choices=category_choices, db_index=True)
    figure = models.URLField('封面图', null=True)
    user = models.ForeignKey(User, verbose_name='人员', on_delete=models.DO_NOTHING)
    news_time = models.DateTimeField('新闻时间', db_index=True, null=True)
    news_text = models.TextField('新闻正文', null=True)
    release_time = models.DateTimeField('发布时间', null=True)
    views_number = models.IntegerField('浏览次数', default=0, null=True)
    explain = models.CharField('说明/摘要/备注', max_length=256, null=True)
    jump_link = models.URLField('跳转链接', null=True)
    news_state = models.IntegerField('新闻发布状态', default=0, choices=news_state_choices, db_index=True)
    examine = models.IntegerField('审核需求', default=0, choices=examine_choices, db_index=True, null=True)
    topping = models.IntegerField('置顶状态', default=2, choices=topping_choices, db_index=True, null=True)
    banner_format = models.IntegerField('banner格式', default=0, choices=banner_format_choices, db_index=True, null=True)
    banner_order = models.IntegerField('banner轮播顺序', default=0, choices=banner_order_choices, db_index=True, null=True)
    release_location = models.IntegerField('发布模块', default=1, choices=release_location_choices, db_index=True, null=True)
    examine_result = models.IntegerField('审核结果', default=0, choices=examine_result_choices, db_index=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-create_time"]


class Attachments(models.Model):
    """
    附件类
    """
    # [news.news_file for news in news.attachments.all()]
    news = models.ForeignKey(News, verbose_name='文章', related_name="attachments", on_delete=models.DO_NOTHING)
    news_file = models.CharField('附件文章', max_length=128)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.news_file

    class Meta:
        ordering = ["-create_time"]