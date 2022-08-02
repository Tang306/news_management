from django.db import models
from account.models import User


class Log(models.Model):
    """
    操作日志类
    """
    create_time = models.DateTimeField('日志创建时间', auto_now_add=True)
    user = models.ForeignKey(User, verbose_name='人员', on_delete=models.DO_NOTHING)
    log_operation = models.CharField('日志操作', max_length=128)
    objects = models.Manager()

    def __str__(self):
        return self.user.username
