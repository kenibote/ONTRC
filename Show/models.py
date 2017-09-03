from django.db import models

# Create your models here.
class odlinfo(models.Model):
    odlname = models.CharField(max_length=30)
    odlip = models.CharField(max_length=20)
    odlport = models.CharField(max_length=10)
    odlkey = models.CharField(max_length=20)
    odlright = models.CharField(max_length=10)
    odlstate = models.CharField(max_length=10)
    def __str__(self):
        return ' Name:'+self.odlname+\
               ' IP:'+self.odlip+':'+self.odlport+\
               ' Code:'+self.odlkey+\
               ' Right:'+self.odlright+\
               ' State:'+self.odlstate


class odlsetlog(models.Model):
    logtime = models.DateField()
    loginfo = models.CharField(max_length=100)



class oeoinfo(models.Model):
    oeoname = models.CharField(max_length=30)
    oeoip = models.CharField(max_length=20)
    oeoport = models.CharField(max_length=10)
    oeokey = models.CharField(max_length=20)
    oeoright = models.CharField(max_length=10)
    oeostate = models.CharField(max_length=10)
    oeotype = models.CharField(max_length=10)
    def __str__(self):
        return ' Name:'+self.oeoname+\
               ' IP:'+self.oeoip+':'+self.oeoport+\
               ' Code:'+self.oeokey+\
               ' Type:'+self.oeotype+ \
               ' Right:'+self.oeoright+\
               ' State:'+self.oeostate


class oeosetlog(models.Model):
    logtime = models.DateField()
    logtype = models.CharField(max_length=20)
    loginfo = models.CharField(max_length=100)