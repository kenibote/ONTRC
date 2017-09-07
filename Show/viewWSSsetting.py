from django.shortcuts import render,HttpResponse
import json,time,Show.communication

from Show import models
# Create your views here.

def wsssetting(req):
    wssinfo1 = models.wssInfo.objects.filter(id=1)
    wssinfo2 = models.wssInfo.objects.filter(id=2)
    wssinfo3 = models.wssInfo.objects.filter(id=3)
    wssinfo4 = models.wssInfo.objects.filter(id=4)

    return render(req,"WSSsetting.html",{
        "wssinfo1":wssinfo1[0],"wssinfo2":wssinfo2[0],
        "wssinfo3": wssinfo3[0],"wssinfo4":wssinfo4[0]
    })


# 当停止OEO服务的时候
def ajax_wsssetting_stop(req):
    # 这里直接在数据库中标记一下即可
    print("WSS服务暂停...")
    deviceid = int(req.POST.get("Device",None))

    if(True):
        # 先修改数据库记录
        models.wssInfo.objects.filter(id=deviceid).update(
            wssstate="OFF"
        )
        # 生成操作记录
        models.wssSetLog.objects.create(
            logtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            loginfo='WSS#'+str(deviceid)+' 服务暂停...' +
                    str(models.wssInfo.objects.filter(id=deviceid)[0]),
            logtype='暂停操作'
        )
        # 生成操作结果
        dic = {"result": "success"}
    else:
        dic = {"result": "error"}
    # 返回操作结果
    time.sleep(2)
    return HttpResponse(json.dumps(dic))


# 当启动WSS服务的时候
def ajax_wsssetting_start(req):
    # 这里尝试发送一个hello包
    print("WSS服务启动...")
    deviceid = int(req.POST.get("Device", None))

    getinfo = models.wssInfo.objects.filter(id=deviceid)[0]
    result = Show.communication.testHello(getinfo.wssip,getinfo.wssport,getinfo.wsskey)

    # 当hello包发送与接收正确的时候
    if(result.startswith("SUCCESS")):
        # 先修改数据库记录
        models.wssInfo.objects.filter(id=deviceid).update(
            wssstate="ON"
        )
        # 然后记录操作
        models.wssSetLog.objects.create(
            logtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            loginfo='WSS#'+str(deviceid)+' 服务启动...' +
                    str(models.wssInfo.objects.filter(id=deviceid)[0]),
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


# 当WSS设置发生变化时候
def ajax_wsssetting_change(req):
    print("WSS信息修改...")

    deviceid = int(req.POST.get("Device", None))
    # TODO 这里可能还需要添加数据验证代码，目前先默认正确
    # 更新数据库数据
    models.wssInfo.objects.filter(id=deviceid).update(
        wsstype=req.POST.get("wsstype", None),
        wssip=req.POST.get("wssip", None),
        wssport=req.POST.get("wssport", None),
        wsskey=req.POST.get("wsskey", None),
        wssright="NULL",
        wssstate="OFF",
        wsslocation=req.POST.get("wsslocation", None)
    )
    # 生成操作日志
    models.wssSetLog.objects.create(
        logtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        loginfo='WSS#'+str(deviceid)+' 信息修改...'+
                str(models.wssInfo.objects.filter(id=deviceid)[0]),
        logtype='信息修改'
    )
    # 返回操作结果
    dic={"result":"success"}
    time.sleep(2)
    return HttpResponse(json.dumps(dic))


# 获取日志信息
def ajax_wsssetting_getlog(req):
    count = models.wssSetLog.objects.count()
    if(count<=10):
        dataraw = models.wssSetLog.objects.all()
    else:
        lastid = models.wssSetLog.objects.last().id
        dataraw = models.wssSetLog.objects.filter(id__gt=(lastid-10))

    data = []
    for e in dataraw:
        data.append(str(e.id))
        data.append(str(e.logtime))
        data.append(e.loginfo)

    # print(data)
    data_ret = {"data":data}
    return HttpResponse(json.dumps(data_ret))