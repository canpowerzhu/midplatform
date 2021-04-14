import oss2
import base64
from common import baseconfig
auth = oss2.Auth(baseconfig.getconfig()['accessKey'], baseconfig.getconfig()['accessSecret'])
bucket = oss2.Bucket(auth, baseconfig.getconfig()['endPoint'], baseconfig.getconfig()['bucketName'])
base_file_url = baseconfig.getconfig()['baseFileUrl']

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
    accessurl = 'midplatform/ApkDir/' + env +'/' + project + '/' + filename
    # 这个是阿里提供的SDK方法 bucket是调用的4.1中配置的变量名

    res = bucket.put_object(accessurl,file,progress_callback=percentage)
    if res.status == 200:
        return base_file_url + accessurl
    else:
        print('fail')
        return False



def uploadBase64Pic(data,projectname='',recordpic=''):
    b64_data = data.split(';base64,')[1]
    logoType = data.split(';base64,')[0].split('/')[1]
    data = base64.b64decode(b64_data)
    import calendar
    import time
    ts = str(calendar.timegm(time.gmtime()))
    if projectname :
        print('项目logo')
        remotePath='midplatform/projectlogo/' + projectname + '.' + logoType
    elif recordpic:
        print('record问题追踪图片')
        remotePath = 'midplatform/recordpic/'+ recordpic +'/' + ts + '.' + logoType
    else:
        print('用户头像')

        remotePath = 'midplatform/avatar/' + ts + '.' + logoType
    res = bucket.put_object(remotePath, data)
    if not res.status == 200:
        return False
    return remotePath




