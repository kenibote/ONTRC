import socket,json,time
from Show import models


# 一个hello测试函数,仅在启动代理的时候使用
def testHello(deviceip,port,key):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 5秒连接超时
    s.settimeout(5)

    try:
        s.connect((deviceip, int(port)))
        message = key+" "+"HELLO\n"
        s.send(message.encode())
        getrespond = s.recv(1024).decode()
        s.close()

        change = json.loads(getrespond)
        if(change.get("result",None)=="SUCCESS"):
            return "SUCCESS"
        else:
            print("鉴权码错误！！！")
            return "FAIL"
    # 如果连接超时
    except socket.timeout as e:
        print("连接超时！！！")
        return "FAIL"
    # 如果结果不符合JSON格式
    except json.JSONDecodeError as e2:
        print("编码错误！！！")
        return "FAIL"


# 一个通用的消息传递函数
def SendAndRec(deviceip,deviceport,message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 8秒连接超时
    s.settimeout(8)

    error = {"result":"FAIL"}
    try:
        s.connect((deviceip, int(deviceport)))
        s.send(message.encode())
        getrespond = s.recv(1024).decode()
        s.close()
        # 转换成json格式
        jsonformate = json.loads(getrespond)
        return jsonformate
    # 如果连接超时
    except socket.timeout as e:
        print("连接超时！！！")
        return error
    # 如果结果不符合JSON格式
    except json.JSONDecodeError as e2:
        print("编码错误！！！")
        return error



def updataOEOinfo():
    result = ""

    oeodevice = models.oeoinfo.objects.all()
    # 对于每一个设备
    for oeo in oeodevice:
        deviceid = str(oeo.id)
        deviceip = str(oeo.oeoip)
        deviceport = int(oeo.oeoport)
        devicekey = str(oeo.oeokey)
        # 如果设备开启
        if(str(oeo.oeostate)=="ON"):
            # 读取设备卡信息
            cards = models.oeoCardInfo.objects.filter(deviceid=deviceid)
            for card in cards:
                # 降低TCP通道数据突发概率
                time.sleep(0.1)
                # "OEO#1 UPDATA SLOT:2\n"
                message_send = devicekey+" UPDATA SLOT:"+str(card.slotid)+"\n"
                print(message_send)
                # 调用通用函数
                respond = SendAndRec(deviceip,deviceport,message_send)

                # 如果返回的数据成功
                if(respond.get("result",None)=="SUCCESS"):
                    # 将波长信息转换为通道id
                    wavecode = str(respond.get("wave"))
                    chanelmap = models.oeoChanelMap.objects.filter(oeocode=wavecode)[0]
                    chanelid = str(chanelmap.chanelid)

                    # 更新链路信息
                    models.oeoCardInfo.objects.filter(
                        deviceid=deviceid, slotid=str(card.slotid)).update(
                        statelocal=respond.get("sfp1"),
                        stateremote=respond.get("sfp2"),
                    )

                    # 如果卡没有被占用，则直接更新信息即可
                    if(str(card.take)=="NO"):
                        models.oeoCardInfo.objects.filter(
                            deviceid=deviceid,slotid=str(card.slotid)).update(
                            chanel = chanelid
                        )
                    else:
                        # TODO 增加修改波长信息
                        # 如果被注册，且本地记录与设备记录不同，则设置设备
                        if(int(chanelid)!=int(card.chanel)):
                            print("远端与本地不同，正在设置远端...")
                            changewave(deviceid,str(card.slotid),str(card.chanel))
                        else:
                            print("远端与本地一样！不用设置")

                else:
                    result = result+"OEO#"+deviceid+" Slot:"+str(card.slotid)+" error"

            result = result+"OEO#"+deviceid+"更新完毕 "
        # 如果设备未开启
        else:
            result = result+"OEO#"+deviceid+"未启动 "
    # 返回结果
    return result



def changewave(device,slot,chanel):
    # 查询OEO通道代码
    chanelmap = models.oeoChanelMap.objects.filter(chanelid=chanel)[0]
    chanelcode = str(chanelmap.oeocode)

    result = "NULL"
    devicedb = models.oeoinfo.objects.filter(id=device)[0]
    # 如果代理启动
    if(str(devicedb.oeostate)=="ON"):
        message = str(devicedb.oeokey)+" CHANGE SLOT:"+slot+" WAVE:"+chanelcode+"\n"
        respond = SendAndRec(str(devicedb.oeoip),
                                           int(devicedb.oeoport),
                                           message)
        # 如果设置指令返回成功
        if(respond.get("result",None)=="SUCCESS"):
            # 进行查询确认
            messagecheck = str(devicedb.oeokey)+" UPDATA SLOT:"+slot+"\n"
            respondcheck = SendAndRec(str(devicedb.oeoip),
                                                    int(devicedb.oeoport),
                                                    messagecheck)
            # 如果检查正确
            if(str(respondcheck.get("wave"))==chanelcode):
                # 更新数据库记录
                models.oeoCardInfo.objects.filter(deviceid=device,slotid=slot).update(
                    chanel = chanel
                )
                print("更新数据库操作执行了。")
                # TODO 补充操作记录 OK
                models.oeoCardLog.objects.create(
                    logtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    deviceid = device,
                    slotid = slot,
                    logtype = "手动修改",
                    loginfo = "通道变为："+chanel
                )
                result = "SUCCESS"
            else:
                result = "FAIL"
        # 如果设置指令失败
        else:
            result = "FAIL"
    # 如果代理没有启动
    else:
        result = "FAIL"

    return result


# 更新WSS信息
def updataWSSinfo():
    result = ""

    wssdevice = models.wssInfo.objects.all()
    # 对于每一个设备
    for wss in wssdevice:
        deviceid = str(wss.id)
        deviceip = str(wss.wssip)
        deviceport = int(wss.wssport)
        devicekey = str(wss.wsskey)
        # 如果设备开启
        if (str(wss.wssstate) == "ON"):
            # 开始循环每一个chanel
            chanel = 1
            while(chanel<=80):
                # 取该chanel的状态
                state = models.wssCardInfo.objects.filter(
                    deviceid=deviceid,chanel=str(chanel))[0]

                # 如果该chanel已被注册，则根据数据库中的信息配置设备
                if(str(state.take)=="YES"):
                    message_send = devicekey + " SET CHANEL:" + str(chanel) + \
                                   " PORT:"+str(state.port) + \
                                   " ATT:"+str(state.att) + "\n"
                    print(message_send)
                    # 调用通用函数
                    respond = SendAndRec(deviceip, deviceport, message_send)

                    if(respond.get("result",None)!="SUCCESS"):
                        result = result + "error in " + deviceid + "#" + str(chanel) + " "

                # 如果该chanel没有被注册，则根据设备的信息更新数据库内容
                else:
                    message_send = devicekey + " CHECK CHANEL:"+ str(chanel) +"\n"
                    print(message_send)
                    # 调用通用函数
                    respond = SendAndRec(deviceip, deviceport, message_send)

                    # 如果返回的数据成功
                    if(respond.get("result",None)=="SUCCESS"):
                        # 更新WSS信息
                        models.wssCardInfo.objects.filter(
                            deviceid=deviceid,chanel=str(chanel)).update(
                            port = respond.get("port",None),
                            att = respond.get("att",None)
                        )
                    else:
                        result = result + "error in "+deviceid+"#"+str(chanel)+" "

                # while指针加1
                chanel+=1


        # 如果设备未开启
        else:
            result = result + "WSS#" + deviceid + "未启动 "

    # 返回结果
    return result



def setWSS(device,chanel,port,att):
    result = "NULL"

    devicedb = models.wssInfo.objects.filter(id=device)[0]
    # 检查代理是否启动
    if(str(devicedb.wssstate)=="ON"):
        message = str(devicedb.wsskey)+" SET CHANEL:"+chanel+" PORT:"+port+" ATT:"+att+"\n"
        respond = SendAndRec(str(devicedb.wssip),int(devicedb.wssport),message)
        # 检查结果
        if(respond.get("result",None)=="SUCCESS"):
            # 更新数据
            models.wssCardInfo.objects.filter(deviceid=device,chanel=chanel).update(
                port = port,
                att = att
            )
            # 记录操作日志
            models.wssCardLog.objects.create(
                logtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                deviceid=device,
                logtype="手动修改",
                loginfo=chanel+"-->"+port+":"+att
            )
            result = "SUCCESS"

        else:
            result =  "FAIL"

    else:
        result =  "FAIL"

    return result

# 生成主页的链路
# TODO 考虑增加一层逻辑：当光路通的时候才显示？
def generate_point():
    lines = []
    lines.append([0,0])

    dataraw = models.lightPathInfo2.objects.all()
    for e in dataraw:
        line = []

        startswitch = models.mainpagepoint.objects.filter(
            devicetype="SWITCH",deviceid=str(e.startswitchid),
            portid=str(e.startswitchport),porttype="OUT")[0]
        line.append([float(startswitch.x),float(startswitch.y)])

        startoeo = models.mainpagepoint.objects.filter(
            devicetype="OEO",deviceid=str(e.startoeoid),
            portid=str(e.startoeoslot),porttype="IN")[0]
        line.append([float(startoeo.x),float(startoeo.y)])
        line.append([float(startoeo.x),float(startoeo.y)+1.02])

        he = models.mainpagepoint.objects.filter(
            devicetype="HE", deviceid=str(e.awgin),portid=str(e.hin))[0]
        line.append([float(he.x),float(he.y)])

        awg = models.mainpagepoint.objects.filter(
            devicetype="HE", deviceid=str(e.awgin), portid="0")[0]
        line.append([float(awg.x), float(awg.y)])

        awgin = models.mainpagepoint.objects.filter(
            devicetype="AWGR", portid=str(e.awgin),porttype="IN")[0]
        line.append([float(awgin.x), float(awgin.y)])

        awgout = models.mainpagepoint.objects.filter(
            devicetype="AWGR", portid=str(e.wssid),porttype="OUT")[0]
        line.append([float(awgout.x), float(awgout.y)])
        line.append([float(awgout.x), float(awgout.y)+0.29])

        wssin = models.mainpagepoint.objects.filter(
            devicetype="WSS", deviceid=str(e.wssid),portid="0")[0]
        line.append([float(wssin.x), float(wssin.y)+1.60])
        line.append([float(wssin.x), float(wssin.y)])

        wssout = models.mainpagepoint.objects.filter(
            devicetype="WSS",deviceid=str(e.wssid),portid=str(e.wssport))[0]
        line.append([float(wssout.x), float(wssout.y)])

        endoeo = models.mainpagepoint.objects.filter(
            devicetype="OEO", deviceid=str(e.endoeoid),
            portid=str(e.endoeoslot),porttype="OUT")[0]
        line.append([float(endoeo.x), float(endoeo.y)+1.02])
        line.append([float(endoeo.x), float(endoeo.y)])

        endswitch = models.mainpagepoint.objects.filter(
            devicetype="SWITCH", deviceid=str(e.endswitchid),
            portid=str(e.endswitchport),porttype="IN")[0]
        line.append([float(endswitch.x), float(endswitch.y)])

        lines.append(line)

    while(len(lines)<=13):
        lines.append([-2,-2])

    return lines


# 生成log页面的加载信息
def loadlogpage(targetid):
    data = []

    if(targetid=="OEO"):
        count = models.oeoCardLog.objects.count()
        if count > 10:
            lastid = models.oeoCardLog.objects.last().id
            dataraw = models.oeoCardLog.objects.filter(id__gt=(lastid-10))
        else:
            dataraw = models.oeoCardLog.objects.all()
        for e in dataraw:
            data.append(str(e.id))
            data.append(str(e.logtime))
            data.append(str(e.logtype))
            message = "Device:"+str(e.deviceid)+" Slot:"+str(e.slotid)+" #"+str(e.loginfo)
            data.append(message)

    if(targetid=="WSS"):
        count = models.wssCardLog.objects.count()
        if count > 10:
            lastid = models.wssCardLog.objects.last().id
            dataraw = models.wssCardLog.objects.filter(id__gt=(lastid-10))
        else:
            dataraw = models.wssCardLog.objects.all()
        for e in dataraw:
            data.append(str(e.id))
            data.append(str(e.logtime))
            data.append(str(e.logtype))
            message = "Device:"+str(e.deviceid)+" #"+str(e.loginfo)
            data.append(message)

    if(targetid=="LightPath"):
        count = models.lightpathlog.objects.count()
        if count > 10:
            lastid = models.lightpathlog.objects.last().id
            dataraw = models.lightpathlog.objects.filter(id__gt=(lastid-10))
        else:
            dataraw = models.lightpathlog.objects.all()
        for e in dataraw:
            data.append(str(e.id))
            data.append(str(e.logtime))
            data.append(str(e.logtype))
            message = str(e.lightpathname)+" "+str(e.loginfo)
            data.append(message)

    return data