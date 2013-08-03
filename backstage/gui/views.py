'''
Created: 2013-06-20
Author: weixin
Email: weixindlut@gmail.com
Desc:

'''
from backstage.backend.logging import loginfo
from django.utils import simplejson
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def upload(request):
    loginfo(p="--" * 10)
    loginfo(p=request)
    loginfo(p="--" * 10)
    if request.method == "POST":
        loginfo(p="**" * 10)
        loginfo(p=request.FILES)
        f = request.FILES["file"]
        with open("/home/amaris/dev/text.cpp", "wb+") as dest:
            for chunk in f.chunks():
                dest.write(chunk)
        data = simplejson.dumps({"status": True})
    else:
        loginfo(p="get")
        data = simplejson.dumps({"status": False})



    return HttpResponse(data, mimetype='application/json')
