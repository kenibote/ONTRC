from django.shortcuts import render,HttpResponse
import json,time

from Show import models
# Create your views here.

# 用于载入odl设置页面
def odlsetting(req):
    odlinfo = models.odlinfo.objects.all()
    return render(req,"ODLsetting.html",{"odlinfo":odlinfo[0]})



# 当停止ODL服务的时候
def ajax_odlsetting_stop(req):
    # TODO 补充停止服务器代码（目前的结构打算只是关闭开关）
    print("ODL服务暂停...")
    if(True):
        # 先修改数据库记录
        models.odlinfo.objects.filter(id=1).update(
            odlstate="off"
        )
        dic = {"result": "success"}
    else:
        dic = {"result": "error"}

    models.odlsetlog.objects.create(
        logtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        loginfo='ODL服务暂停...' + str(models.odlinfo.objects.last()),
        logtype='服务暂停'
    )
    time.sleep(3)
    return HttpResponse(json.dumps(dic))



# 当启动ODL服务的时候
def ajax_odlsetting_start(req):
    # TODO 补充启动服务器代码（进行连通性测试）
    print("ODL服务启动...")

    if(True):
        # 先修改数据库记录
        models.odlinfo.objects.filter(id=1).update(
            odlstate="on"
        )
        dic = {"result": "success"}
    else:
        dic = {"result": "error"}

    models.odlsetlog.objects.create(
        logtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        loginfo='ODL服务启动...' + str(models.odlinfo.objects.last()),
        logtype='服务启动'
    )
    time.sleep(3)
    return HttpResponse(json.dumps(dic))



# 当ODL信息发生修改时
def ajax_odlsetting_change(req):
    print("ODL信息修改...")

    if req.method=="POST":
        #print(req.POST)
        # TODO 这里可能还需要添加数据验证代码，目前先默认正确
        models.odlinfo.objects.filter(id=1).update(
            odltype=req.POST.get("odltype", None),
            odlip=req.POST.get("odlip", None),
            odlport=req.POST.get("odlport", None),
            odlkey=req.POST.get("odlkey", None),
            odlright="NULL",
            odlstate="off",
            odllocation=req.POST.get("odllocation",None)
        )
        dic={"result":"success"}

    models.odlsetlog.objects.create(
        logtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        loginfo='ODL信息修改...'+str(models.odlinfo.objects.last()),
        logtype='信息修改'
    )
    time.sleep(3)
    return HttpResponse(json.dumps(dic))

# 获取日志信息
def ajax_odlsetting_getlog(req):
    count = models.odlsetlog.objects.count()
    if(count<=10):
        dataraw = models.odlsetlog.objects.all()
    else:
        lastid = models.odlsetlog.objects.last().id
        dataraw = models.odlsetlog.objects.filter(id__gt=(lastid-10))

    data = []
    for e in dataraw:
        data.append(str(e.id))
        data.append(str(e.logtime))
        data.append(e.loginfo)

    # print(data)
    data_ret = {"data":data}
    return HttpResponse(json.dumps(data_ret))
