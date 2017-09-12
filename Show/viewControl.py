from django.shortcuts import render,HttpResponse
import json,time,threading
from socket import *
from Show import models,communication

def control(req):

    return render(req,"control.html")

# 后台守护程序UDP监听OEO的TRAP数据包
def udpthread(HOST,PORT):
    BUFSIZ = 1024
    ADDR = (HOST, PORT)

    # 创建一个服务器端UDP套接字
    udpServer = socket(AF_INET, SOCK_DGRAM)
    # 绑定服务器套接字
    udpServer.bind(ADDR)
    # b'OEO:1 SLOT:4 EVENT:1.3.6.1.4.1.6688.1.1.2.83'
    while True:
        print('waiting for message...')
        # 接收来自客户端的数据
        data, addr = udpServer.recvfrom(BUFSIZ)
        # 打印结果
        raw = str(data)[2:-1]
        print(raw)
        # 检查数据合法性
        if(raw.startswith("OEO")):
            info = raw.split(" ")
            oeo = str(info[0].split(":")[1])
            slot = str(info[1].split(":")[1])
            event = int(info[2].split(":")[1].split(".")[10])
            if(event==81):
                models.oeoCardInfo.objects.filter(deviceid=oeo,slotid=slot).update(statelocal="UP")
            if(event==82):
                models.oeoCardInfo.objects.filter(deviceid=oeo, slotid=slot).update(statelocal="DOWN")
            if(event==83):
                models.oeoCardInfo.objects.filter(deviceid=oeo, slotid=slot).update(stateremote="UP")
            if(event==84):
                models.oeoCardInfo.objects.filter(deviceid=oeo, slotid=slot).update(stateremote="DOWN")
            # 将记录写入数据库
            models.oeoCardLog.objects.create(
                logtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                deviceid = oeo,
                slotid = slot,
                logtype = "Trap",
                loginfo = event
            )

            print("数据更新完毕...")


# 隐藏入口，启动UDP监听程序
UDPSERVRT = 0
Thread = 0
def snmpudp(req):
    global UDPSERVRT
    global Thread

    if(UDPSERVRT==0):
        # 如果线程没有启动，则启动线程
        UDPSERVRT = 1
        Thread = threading.Thread(target=udpthread, args=("10.10.12.25",8099,))
        Thread.setDaemon(True)
        Thread.start()
        print("线程启动成功！")
        return render(req,"UDP.html",{"info":"线程启动成功！"})
    else:
        print("线程已经启动！")
        return render(req, "UDP.html", {"info": "线程已经启动！"})




# 从数据库载入OEO信息
def ajax_control_loadoeoinfo(req):
    deviceid = int(req.POST.get("Device",None))
    dataraw = models.oeoCardInfo.objects.filter(deviceid=deviceid)

    data = []
    for e in dataraw:
        data.append(str(e.slotid))
        data.append(str(e.chanel))
        wave = "NULL"
        if(str(e.chanel)!="NULL"):
            wave = models.oeoChanelMap.objects.filter(
                chanelid=str(e.chanel))[0].wavelength
        data.append(wave)
        data.append(str(e.statelocal))
        data.append(str(e.stateremote))
        data.append(str(e.take))

    # print(data)
    data_ret = {"data":data}
    return HttpResponse(json.dumps(data_ret))


# 更新OEO信息
def ajax_control_updataoeoinfo(req):
    data = communication.updataOEOinfo()
    data_ret = {"data": data}
    return HttpResponse(json.dumps(data_ret))

# 更新WSS信息
def ajax_control_updatawssinfo(req):
    data = communication.updataWSSinfo()
    data_ret = {"data": data}
    return HttpResponse(json.dumps(data_ret))


# 从数据库载入WSS信息







# 设置OEO波长
def ajax_control_setoeo(req):
    # 获取网页端信息
    device = str(req.POST.get("Device",None))
    slot = str(req.POST.get("Slot",None))
    chanel = str(req.POST.get("Chanel",None))

    data = communication.changewave(device,slot,chanel)
    print(data)
    data_ret = {"data": data}
    return HttpResponse(json.dumps(data_ret))

# 设置WSS
def ajax_control_setwss(req):
    device = str(req.POST.get("Device",None))
    chanel = str(req.POST.get("Chanel",None))
    port = str(req.POST.get("Port",None))
    att = str(req.POST.get("Att",None))

    data = communication.setWSS(device,chanel,port,att)
    print(data)
    data_ret = {"data": data}
    return HttpResponse(json.dumps(data_ret))


# 增加光路
def ajax_control_addlightpath(req):
    print(req.POST)

    result = "SUCCESS"

    lightpathname = str(req.POST.get("name",None))

    startswitchid = str(req.POST.get("startswitchid",None))
    startswitchport = str(req.POST.get("startswitchport", None))
    startoeoid = str(req.POST.get("startoeoid", None))
    startoeoslot = str(req.POST.get("startoeoslot", None))

    awgin = str(req.POST.get("awgin", None))
    he = str(req.POST.get("he", None))
    wssid = str(req.POST.get("wssid", None))
    wssport = str(req.POST.get("wssport", None))
    att = str(req.POST.get("att", None))
    chanel = str(req.POST.get("chanel", None))

    endoeoid = str(req.POST.get("endoeoid", None))
    endoeoslot = str(req.POST.get("endoeoslot", None))
    endswitchid = str(req.POST.get("endswitchid", None))
    endswitchport = str(req.POST.get("endswitchport", None))


    # 检查起始端OEO状态
    startoeo = models.oeoCardInfo.objects.filter(deviceid=startoeoid,slotid=startoeoslot)
    if(str(startoeo[0].take)=="YES"):
        result = "FAIL"

    # 检查该WSS通道状态
    wssstate = models.wssCardInfo.objects.filter(deviceid=wssid,chanel=chanel)
    if(str(wssstate[0].take)=="YES"):
        result = "FAIL"


    # TODO 调用设置OEO和WSS的程序


    if(result=="SUCCESS"):
        # 登记光路信息
        models.lightPathInfo2.objects.create(
            name = lightpathname,
            startswitchid = startswitchid,
            startswitchport = startswitchport,
            startoeoid = startoeoid,
            startoeoslot = startoeoslot,
            awgin = awgin,
            hin = he,
            wssid = wssid,
            wssport = wssport,
            endoeoid = endoeoid,
            endoeoslot = endoeoslot,
            endswitchid = endswitchid,
            endswitchport = endswitchport,
            att = att,
            chanel = chanel,
            state = "NULL"
        )

        # 登记注册信息
        startoeo.update(take = "YES")
        wssstate.update(take = "YES")


    data_ret = {"data": result}
    return HttpResponse(json.dumps(data_ret))


# TODO 修改光路，删除光路的操作
# TODO OEO链路的状态会影响到光路的状态，注意增加相关代码
# TODO 其实，lightpath中记录的链路状态信息基本无关，在向网页载入数据的时候，直接检查oeo数据库中记录的链路信息即可