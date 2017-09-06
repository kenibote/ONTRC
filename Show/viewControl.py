from django.shortcuts import render,HttpResponse
import json,time
from Show import models

def control(req):

    return render(req,"control.html")






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


def ajax_control_updataoeoinfo(req):


    # print(data)
    data_ret = {"data": "SUCCESS"}
    return HttpResponse(json.dumps(data_ret))