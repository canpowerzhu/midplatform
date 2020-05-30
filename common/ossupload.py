import oss2
from sysconf import models
from django.forms.models import model_to_dict
import hashlib
import base64
#
res = model_to_dict(models.ossconf.objects.first())
accessKey = res['accessKey']
accessSecret = res['accessSecret']
endPoint = res['endPoint']
bucketName = res['bucketName']
auth = oss2.Auth(accessKey, accessSecret)
bucket = oss2.Bucket(auth, endPoint, bucketName)
base_file_url = 'https://moppowar.oss-accelerate.aliyuncs.com/'

def percentage(consumed_bytes, total_bytes):
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        print('\r{0}% '.format(rate), end='')


def update_fil_file(envtype,project,filename,file):
    """
    :param envtype: 环境类型
    :param project: 项目名称
    :param filename: 文件名称
    :param file: 文件流
    :return:
    """
    print(envtype,type(envtype))
    if envtype == 1:
        env = 'online'
    elif envtype == 0:
        env = 'offline'
    accessurl = 'ApkDir/' + env +'/' + project + '/' + filename
    # 这个是阿里提供的SDK方法 bucket是调用的4.1中配置的变量名

    res = bucket.put_object(accessurl,file,progress_callback=percentage)
    if res.status == 200:
        return base_file_url + accessurl
    else:
        print('fail')
        return False



def uploadBase64Pic(projectname,data):
    b64_data = data.split(';base64,')[1]
    logoType = data.split(';base64,')[0].split('/')[1]
    data = base64.b64decode(b64_data)
    remotePath='projectlogo/' + projectname + '.' + logoType
    res = bucket.put_object(remotePath, data)
    if not res.status == 200:
        return False
    return remotePath


