from django.db import models

# Create your models here.

# ODL配置信息
class odlinfo(models.Model):
    odltype = models.CharField(max_length=20)
    odlip = models.CharField(max_length=20)
    odlport = models.CharField(max_length=10)
    odlkey = models.CharField(max_length=20)
    # 目前right这个字段没有用到
    odlright = models.CharField(max_length=10)
    odlstate = models.CharField(max_length=10)
    odllocation = models.CharField(max_length=20)
    def __str__(self):
        return ' Type:'+self.odltype+\
               ' IP:'+self.odlip+':'+self.odlport+\
               ' Code:'+self.odlkey+\
               ' Location:'+self.odllocation+\
               ' State:'+self.odlstate

# ODL配置日志
class odlsetlog(models.Model):
    logtime = models.CharField(max_length=40)
    logtype = models.CharField(max_length=20)
    loginfo = models.CharField(max_length=100)


# OEO配置信息
class oeoinfo(models.Model):
    oeotype = models.CharField(max_length=20)
    oeoip = models.CharField(max_length=20)
    oeoport = models.CharField(max_length=10)
    oeokey = models.CharField(max_length=20)
    # 目前right这个字段没有用到
    oeoright = models.CharField(max_length=10)
    oeostate = models.CharField(max_length=10)
    oeolocation = models.CharField(max_length=20)
    def __str__(self):
        return ' Type:'+self.oeotype+\
               ' IP:'+self.oeoip+':'+self.oeoport+\
               ' Code:'+self.oeokey+\
               ' Location:'+self.oeolocation+ \
               ' State:'+self.oeostate

# TODO 补充OEO基本状态信息 电源，风扇，温度

# OEO配置日志
class oeosetlog(models.Model):
    logtime = models.CharField(max_length=40)
    logtype = models.CharField(max_length=20)
    loginfo = models.CharField(max_length=100)


# 帮助信息数据库
class help(models.Model):
    helptitle = models.CharField(max_length=50)
    helpkeyword = models.CharField(max_length=50)
    helptxt = models.TextField()


# OEO板卡状态信息
# TODO 这个数据结构有问题
class oeoCard(models.Model):
    # 该板卡属于哪一个OEO代理
    oeoCardBelong = models.CharField(max_length=10)
    # 该板卡在该代理下的id号
    oeoCardInerId = models.CharField(max_length=10)
    # 本地连接了哪一台交换机
    oeoCardLocal = models.CharField(max_length=20)
    # 该板卡连接了AWGR的哪一个输入口
    oeoCardOutPort = models.CharField(max_length=10)
    # 该板卡连接了哪一个WSS
    oeoCardInWss = models.CharField(max_length=10)
    # 该板卡连接了WSS的哪一个输出口
    oeoCardInWssPort = models.CharField(max_length=10)
    # 该板卡的工作波长
    # TODO 这里可以建一张字典对应关系表
    oeoCardFrequency = models.IntegerField()
    # 该板卡的工作状态
    oeoCardState = models.CharField(max_length=10)


class oeoChanelMap(models.Model):
    chanelid = models.CharField(max_length=10)
    wavelength = models.CharField(max_length=20)
    oeocode = models.CharField(max_length=20)
    wsscode = models.CharField(max_length=20)


class oeoHealthLog(models.Model):
    logtime = models.CharField(max_length=40)
    deviceid = models.CharField(max_length=10)
    powerA = models.CharField(max_length=10)
    powerB = models.CharField(max_length=10)
    fan = models.CharField(max_length=10)
    tempture = models.CharField(max_length=10)


class oeoCardInfo(models.Model):
    deviceid = models.CharField(max_length=10)
    slotid = models.CharField(max_length=10)
    # 这里记录的是chanelid 这是唯一编号
    chanel = models.CharField(max_length=10)
    statelocal = models.CharField(max_length=10)
    stateremote = models.CharField(max_length=10)
    take = models.CharField(max_length=10)


class oeoCardLog(models.Model):
    logtime = models.CharField(max_length=40)
    deviceid = models.CharField(max_length=10)
    slotid = models.CharField(max_length=10)
    logtype = models.CharField(max_length=20)
    loginfo = models.CharField(max_length=100)