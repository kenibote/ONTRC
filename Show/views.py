from django.shortcuts import render,HttpResponse
import json,time

from Show import models
# Create your views here.
def test(req):

    return render(req,"Test.html")

def pagenotfound(req):
    return render(req,"404.html")


def index(req):

    return render(req,"index.html")

def control(req):

    return render(req,"control.html")


def logging(req):

    return render(req,"logging.html")


def setting(req):
    # TODO 这里还需要补充WSS的内容
    # TODO 补充资源利用率代码
    odlinfo = models.odlinfo.objects.all()
    oeoinfo1 = models.oeoinfo.objects.filter(id=1)
    oeoinfo2 = models.oeoinfo.objects.filter(id=2)
    return render(req,"setting.html",{"odlinfo":odlinfo[0],
                                      "oeoinfo1":oeoinfo1[0],
                                      "oeoinfo2":oeoinfo2[0]})


def help(req):
    author = models.help.objects.filter(id=1)
    info = models.help.objects.filter(id__gt=1)
    return render(req,"help.html",{"author":author[0],"info":info})

# 对于空连接，直接返回主页
def NoneMainPage(req):
    return render(req,"index.html")