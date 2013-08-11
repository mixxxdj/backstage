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
from backstage.deploy import DBConfig as dbc


@csrf_exempt
def upload(request):
    if request.method == "POST":
        f = request.raw_post_data.split("&", 1)
        loginfo(f[0])
        fileName = os.path.basename(f[0])
        path = os.path.join(settings.TMP_FILE_PATH, fileName)
        with open(path, "wb+") as dest:
            dest.write(f[1])
        if len(fileName) >= 9 and cmp(fileName[-9], '.midi.xml') == 0:
            pid = dbc.importOnePreset(path)
            if pid != '':
                data = simplejson.dumps({"status": True,
                                         "info": pid})
            else:
                data = simplejson.dumps({"status": False,
                                         "info": 'The preset name has been used!'})
        else:
            data = simplejson.dumps({"status":True,"info":'success'})
    else:
        loginfo(p="get")
        data = simplejson.dumps({"status": False,
                                 "info": 'Error request'})
    return HttpResponse(data, mimetype='application/json')
