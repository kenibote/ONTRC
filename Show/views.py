from django.shortcuts import render

# Create your views here.
def test(req):

    return render(req,"Test.html")


def index(req):

    return render(req,"index.html")

def control(req):

    return render(req,"control.html")


def logging(req):

    return render(req,"logging.html")


def setting(req):

    return render(req,"setting.html")


def help(req):

    return render(req,"help.html")