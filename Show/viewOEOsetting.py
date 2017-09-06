from django.shortcuts import render,HttpResponse
import json,time, Show.communication

from Show import models
# Create your views here.

def oeosetting(req):
    oeoinfo1 = models.oeoinfo.objects.filter(id=1)
    oeoinfo2 = models.oeoinfo.objects.filter(id=2)
    return render(req,"OEOsetting.html",
                  {"oeoinfo1":oeoinfo1[0],"oeoinfo2":oeoinfo2[0]})


# 当停止OEO服务的时候
def ajax_oeosetting_stop(req):
    # 这里直接在数据库中标记一下即可
    print("OEO服务暂停...")
    deviceid = int(req.POST.get("Device",None))

    if(True):
        # 先修改数据库记录
        models.oeoinfo.objects.filter(id=deviceid).update(
            oeostate="OFF"
        )
        # 生成操作记录
        models.oeosetlog.objects.create(
            logtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            loginfo='OEO#'+str(deviceid)+' 服务暂停...' +
                    str(models.oeoinfo.objects.filter(id=deviceid)[0]),
            logtype='暂停操作'
        )
        # 生成操作结果
        dic = {"result": "success"}
    else:
        dic = {"result": "error"}
    # 返回操作结果
    time.sleep(2)
    return HttpResponse(json.dumps(dic))



# 当启动OEO服务的时候
def ajax_oeosetting_start(req):
    # 这里尝试发送一个hello包
    print("OEO服务启动...")
    deviceid = int(req.POST.get("Device", None))

    getinfo = models.oeoinfo.objects.filter(id=deviceid)[0]
    result = Show.communication.testHello(getinfo.oeoip,getinfo.oeoport,getinfo.oeokey)

    # 当hello包发送与接收正确的时候
    if(result.startswith("SUCCESS")):
        # 先修改数据库记录
        models.oeoinfo.objects.filter(id=deviceid).update(
            oeostate="ON"
        )
        # 然后记录操作
        models.oeosetlog.objects.create(
            logtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            loginfo='OEO#'+str(deviceid)+' 服务启动...' +
                    str(models.oeoinfo.objects.filter(id=deviceid)[0]),
            logtype='启动操作'
        )
        # 生成操作结果
        dic = {"result": "success"}
    else:
        # 如果失败则什么也不操作，直接返回操作失败结果
        dic = {"result": "error"}
    # 返回操作结果
    time.sleep(2)
    return HttpResponse(json.dumps(dic))



# 当OEO设置发生变化时候
def ajax_oeosetting_change(req):
    print("OEO信息修改...")

    deviceid = int(req.POST.get("Device", None))
    # TODO 这里可能还需要添加数据验证代码，目前先默认正确
    # 更新数据库数据
    models.oeoinfo.objects.filter(id=deviceid).update(
        oeotype=req.POST.get("oeotype", None),
        oeoip=req.POST.get("oeoip", None),
        oeoport=req.POST.get("oeoport", None),
        oeokey=req.POST.get("oeokey", None),
        oeoright="NULL",
        oeostate="OFF",
        oeolocation=req.POST.get("oeolocation", None)
    )
    # 生成操作日志
    models.oeosetlog.objects.create(
        logtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        loginfo='OEO#'+str(deviceid)+' 信息修改...'+
                str(models.oeoinfo.objects.filter(id=deviceid)[0]),
        logtype='信息修改'
    )
    # 返回操作结果
    dic={"result":"success"}
    time.sleep(2)
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