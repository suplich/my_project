﻿# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import os
import uuid
import json
import datetime as dt


#装饰器 不知道干嘛的
@csrf_exempt
def upload_image(request, dir_name):
    ##################
    #  kindeditor图片上传返回数据格式说明：
    # {"error": 1, "message": "出错信息"}
    # {"error": 0, "url": "图片地址"}
    ##################
    result = {"error": 32111, "message": "wocao"}
    files = request.FILES.get("imgFile", None)
    if files:
        result =image_upload(files, dir_name)
    return HttpResponse(json.dumps(result), content_type="application/json")


#目录创建
def upload_generation_dir(dir_name):
    today = dt.datetime.today()
    dir_name = dir_name + '/%d/%d/' %(today.year,today.month)
    if not os.path.exists(settings.MEDIA_ROOT +'/'+dir_name):
        os.makedirs(settings.MEDIA_ROOT + '/'+dir_name)
    return dir_name


# 图片上传
def image_upload(files, dir_name):
    #允许上传文件类型
    print dir_name
    print settings.MEDIA_ROOT+'/'+dir_name
    allow_suffix =['jpg', 'png', 'jpeg', 'gif', 'bmp']
    file_suffix = files.name.split(".")[-1]
    if file_suffix not in allow_suffix:
        return {"error": 1, "message": "格式错误"}
    relative_path_file = upload_generation_dir(dir_name)
    print relative_path_file
    path=os.path.join(settings.MEDIA_ROOT, relative_path_file)
    if not os.path.exists(path): #如果目录不存在创建目录
        os.makedirs(path)
    file_name=str(uuid.uuid1())+"."+file_suffix
    path_file=os.path.join(path, file_name)
    file_url = settings.MEDIA_URL + relative_path_file + file_name
    open(path_file, 'wb').write(files.file.read()) # 保存图片
    return {"error": 0, "url": file_url}
    return {"error": 0, "url": "caonima"}
