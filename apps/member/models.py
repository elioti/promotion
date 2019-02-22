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
    TYPE_CHOICES = (
        (0, "自然抽奖"),
        (1, "内定抽奖"),
        (2, "后台添加")
    )
    SEND_CHOICES = (
        (0, "未派送"),
        (1, "已派送")
    )
    user = models.CharField('活动用户', max_length=32)
    prizeName = models.CharField('奖品名称', max_length=64)
    prizeId = models.IntegerField('奖品ID', default=None)
    datetime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    sendTime = models.DateTimeField(verbose_name='发送时间', null=True, default=None)
    isSend = models.IntegerField('是否发送', choices=SEND_CHOICES, default=0)
    ip = models.GenericIPAddressField(verbose_name='抽奖IP')
    type = models.IntegerField('抽奖方式', choices=TYPE_CHOICES, default=0)

    class Meta:
        verbose_name = '活动记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user+"#"+self.prizeName
