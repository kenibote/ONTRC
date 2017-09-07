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
        Thread = threading.Thread(target=udpthread, args=("10.10.12.20",8099,))
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