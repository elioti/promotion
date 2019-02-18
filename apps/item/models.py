from django.db import models

# Create your models here.


class Prize(models.Model):
    """礼品模型类"""
    code = models.IntegerField(default=None, verbose_name='礼品编号', unique=True)
    prize_name = models.CharField(max_length=64, verbose_name='礼品名称')
    probability = models.IntegerField('中奖概率', default=0)

    class Meta:
        verbose_name = '奖品管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.prize_name


class Info(models.Model):
    """
    活动时间、文本配置
    """
    name = models.CharField(max_length=32, verbose_name='活动名称')
    is_open = models.BooleanField(default=False, verbose_name='是否开启')
    errmsg = models.CharField(max_length=100, verbose_name='关闭提示')
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')


