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
    name = models.CharField(max_length=32, verbose_name='活动名称',default='请设置活动名称')
    is_open = models.BooleanField(default=False, verbose_name='是否开启')
    errmsg = models.CharField(max_length=100, verbose_name='关闭提示',default='活动还未开启')
    start_time = models.DateTimeField(verbose_name='开始时间', null=True, default=None)
    end_time = models.DateTimeField(verbose_name='结束时间', null=True, default=None)


class Rule(models.Model):
    """
    内定规则
    """
    user = models.CharField('活动用户', max_length=32)
    sequence = models.CharField('顺序', max_length=64, default='')
    flag = models.IntegerField('标记', default=1)
    score = models.IntegerField("活动次数", default=0)
    addTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def get_order(self):
        order_list = self.sequence.split('.')
        if 0 < self.flag <= len(order_list):
            order = order_list[self.flag-1]
            self.flag = self.flag + 1
            if len(order.strip()) == 0:
                return None
            else:
                return int(order)
        else:
            return None

    class Meta:
        verbose_name = '活动用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.user)



