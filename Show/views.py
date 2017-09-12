from django.shortcuts import render,HttpResponse
import json,time

from Show import models
# Create your views here.
def test(req):

    return render(req,"Test.html")

def pagenotfound(req):
    return render(req,"404.html")


def index(req):
    lp1 = [[-0.5,-0.1],[0.2,1.1],[0.2,2.1],[0.2,3.6],[0.47,3.9],[0.47,4.6],[3.05,6.0],[3.05,6.35],[4.35,5.8],[4.35,4.2],[4.1,3.6],[3.25,2.1],[3.25,1.1],[3.0,-0.1]]
    lp2 = [[0.1,-0.1],[0.8,1.1],[0.8,2.1],[0.4,3.6],[0.47,3.9],[0.47,4.6],[5.59,6.0],[5.59,6.35],[6.9,5.8],[6.9,4.2],[7.1,3.6],[7.42,2.1],[7.42,1.1],[7.0,-0.1]]
    lp3 = [[-1,-1],[-1,-2]]
    lp4 = [[-1, -1],[-1,-2]]
    return render(req,"index.html",{"lp1":lp1,"lp2":lp2,"lp3":lp3,"lp4":lp4})


def logging(req):

    return render(req,"logging.html")


def setting(req):
    # TODO 这里还需要补充WSS的内容
    # TODO 补充资源利用率代码
    odlinfo = models.odlinfo.objects.all()

    oeoinfo1 = models.oeoinfo.objects.filter(id=1)
    oeoinfo2 = models.oeoinfo.objects.filter(id=2)

    wssinfo1 = models.wssInfo.objects.filter(id=1)
    wssinfo2 = models.wssInfo.objects.filter(id=2)
    wssinfo3 = models.wssInfo.objects.filter(id=3)
    wssinfo4 = models.wssInfo.objects.filter(id=4)
    return render(req,"setting.html",{"odlinfo":odlinfo[0],
                                      "oeoinfo1":oeoinfo1[0],
                                      "oeoinfo2":oeoinfo2[0],
                                      "wssinfo1": wssinfo1[0],
                                      "wssinfo2": wssinfo2[0],
                                      "wssinfo3": wssinfo3[0],
                                      "wssinfo4": wssinfo4[0]})


def help(req):
    author = models.help.objects.filter(id=1)
    info = models.help.objects.filter(id__gt=1)
    return render(req,"help.html",{"author":author[0],"info":info})

# 对于空连接，直接返回主页
def NoneMainPage(req):
    return render(req,"index.html")