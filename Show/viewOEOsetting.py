from django.shortcuts import render,HttpResponse
import json,time

from Show import models
# Create your views here.

def oeosetting(req):
    oeoinfo1 = models.oeoinfo.objects.filter(id=1)
    oeoinfo2 = models.oeoinfo.objects.filter(id=2)
    return render(req,"OEOsetting.html",
                  {"oeoinfo1":oeoinfo1[0],"oeoinfo2":oeoinfo2[0]})


# 当停止OEO服务的时候
def ajax_oeosetting_stop(req):
    # TODO 补充停止服务器代码
    print("OEO服务暂停...")
    deviceid = int(req.POST.get("Device",None))

    if(True):
        # 先修改数据库记录
        models.oeoinfo.objects.filter(id=deviceid).update(
            oeoright="yes",
            oeostate="off"
        )
        dic = {"result": "success"}
    else:
        dic = {"result": "error"}

    models.oeosetlog.objects.create(
        logtime=time.strftime("%Y-%m-%d", time.localtime()),
        loginfo='OEO#'+str(deviceid)+' 服务暂停...' +
                str(models.oeoinfo.objects.filter(id=deviceid)[0]),
        logtype='暂停操作'
    )
    time.sleep(3)
    return HttpResponse(json.dumps(dic))



# 当启动OEO服务的时候
def ajax_oeosetting_start(req):
    # TODO 补充启动服务器代码
    print("OEO服务启动...")
    deviceid = int(req.POST.get("Device", None))

    if(True):
        # 先修改数据库记录
        models.oeoinfo.objects.filter(id=deviceid).update(
            oeoright="yes",
            oeostate="on"
        )
        dic = {"result": "success"}
    else:
        dic = {"result": "error"}

    models.oeosetlog.objects.create(
        logtime=time.strftime("%Y-%m-%d", time.localtime()),
        loginfo='OEO#'+str(deviceid)+' 服务启动...' +
                str(models.oeoinfo.objects.filter(id=deviceid)[0]),
        logtype='启动操作'
    )
    time.sleep(3)
    return HttpResponse(json.dumps(dic))



# 当OEO设置发生变化时候
def ajax_oeosetting_change(req):
    print("OEO信息修改...")

    if req.method=="POST":
        #print(req.POST)
        deviceid = int(req.POST.get("Device", None))
        # TODO 这里可能还需要添加数据验证代码，目前先默认正确
        models.oeoinfo.objects.filter(id=deviceid).update(
            oeoname=req.POST.get("oeoname", None),
            oeoip=req.POST.get("oeoip", None),
            oeoport=req.POST.get("oeoport", None),
            oeokey=req.POST.get("oeokey", None),
            oeoright="no",
            oeostate="off"
        )
        dic={"result":"success"}

    models.oeosetlog.objects.create(
        logtime=time.strftime("%Y-%m-%d", time.localtime()),
        loginfo='OEO#'+str(deviceid)+' 信息修改...'+
                str(models.oeoinfo.objects.filter(id=deviceid)[0]),
        logtype='信息修改'
    )
    time.sleep(3)
    return HttpResponse(json.dumps(dic))



# 获取日志信息
def ajax_oeosetting_getlog(req):
    count = models.oeosetlog.objects.count()
    if(count<=10):
        dataraw = models.oeosetlog.objects.all()
    else:
        lastid = models.oeosetlog.objects.last().id
        dataraw = models.oeosetlog.objects.filter(id__gt=(lastid-10))

    data = []
    for e in dataraw:
        data.append(str(e.id))
        data.append(str(e.logtime))
        data.append(e.loginfo)

    # print(data)
    data_ret = {"data":data}
    return HttpResponse(json.dumps(data_ret))