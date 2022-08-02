from django.db import models


class User(models.Model):
    """
    用户类
    """
    state_choices = ((1, '超级管理员'), (2, '发布员'), (3, '审核员'), (-1, '无效用户'), (-2, '删除账号'))

    username = models.CharField('用户名', max_length=128, unique=True)
    nickname = models.CharField('昵称', max_length=128, null=True)
    password = models.CharField('密码', max_length=128)
    state = models.IntegerField('用户状态', default=1, choices=state_choices, db_index=True)
    last_login = models.DateTimeField('上次登录时间', null=True, db_index=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["-create_time"]