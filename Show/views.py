from django.shortcuts import render,HttpResponse
import json,time
from Show import communication

from Show import models
# Create your views here.
def test(req):
    return render(req,"Test.html")

def pagenotfound(req):
    return render(req,"404.html")


def index(req):
    lp = communication.generate_point()
    # print(lp)
    return render(req,"index.html",{"lp1":lp[1],"lp2":lp[2],"lp3":lp[3],"lp4":lp[4],
                                    "lp5": lp[5], "lp6": lp[6], "lp7": lp[7], "lp8": lp[8],
                                    "lp9": lp[9], "lp10": lp[10], "lp11": lp[11], "lp12": lp[12],})


def logging(req):
    return render(req,"logging.html")

def ajax_logging_loadlog(req):
    targetid = str(req.POST.get("Device",None))
    data = communication.loadlogpage(targetid)
    data_ret = {"data": data}
    return HttpResponse(json.dumps(data_ret))


def setting(req):
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
    lp = communication.generate_point()
    # print(lp)
    return render(req,"index.html",{"lp1":lp[1],"lp2":lp[2],"lp3":lp[3],"lp4":lp[4],
                                    "lp5": lp[5], "lp6": lp[6], "lp7": lp[7], "lp8": lp[8],
                                    "lp9": lp[9], "lp10": lp[10], "lp11": lp[11], "lp12": lp[12],})