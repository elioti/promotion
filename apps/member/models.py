from django.db import models

# Create your models here.


class Member(models.Model):
    """
    活动用户
    """
    username = models.CharField("会员账号", max_length=32)
    score = models.IntegerField("活动次数", default=0)

    class Mete:
        verbose_name = "活动用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.username)


class Rec(models.Model):
    """
    活动记录
    """
    user = models.CharField('活动用户', max_length=32)
    prize_name = models.CharField('奖品名称', max_length=64)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    send_time = models.DateTimeField(verbose_name='发送时间', null=True, default=None)
    is_sent = models.BooleanField(default=False, verbose_name='是否发送')
    user_ip = models.GenericIPAddressField(verbose_name='抽奖IP')
    way = models.CharField(max_length=100, default='自然抽奖', verbose_name='抽奖方式')

    class Meta:
        verbose_name = '活动记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user+"#"+self.prize_name
