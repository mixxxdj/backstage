'''
Created: 2013-06-20
Author: weixin
Email: weixindlut@gmail.com
Desc:

'''
import uuid
import os
from django.conf import settings
from backstage.backend.logging import loginfo
from django.utils import simplejson
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def upload(request):
    if request.method == "POST":
        f = request.raw_post_data.split("&", 1)
        loginfo(f[0])
        path = os.path.join(settings.TMP_FILE_PATH, f[0])
        with open(path, "wb+") as dest:
            dest.write(f[1])
        data = simplejson.dumps({"status": True})
    else:
        loginfo(p="get")
        data = simplejson.dumps({"status": False})

    return HttpResponse(data, mimetype='application/json')
