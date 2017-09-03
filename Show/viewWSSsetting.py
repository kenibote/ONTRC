from django.shortcuts import render,HttpResponse
import json,time

from Show import models
# Create your views here.

def wsssetting(req):

    return render(req,"WSSsetting.html")