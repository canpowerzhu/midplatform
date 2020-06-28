# @Author  : kane.zhu
# @Time    : 2020/6/24 18:23
# @Software: PyCharm
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import os,requests, time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor,ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from urllib import parse
# BlockingScheduler 此程序会阻塞
# BackgroundScheduler 不会阻塞

jobstores={
    #这里要存储到Mysql存储内
    'default':SQLAlchemyJobStore(url='mysql://root:{}@192.168.1.5:3306/midplatform'.format(parse.quote('123Moppo!@#')))
}

executors = {
     'default': ThreadPoolExecutor(20),
     'processpool': ProcessPoolExecutor(5)
   }

job_defaults = {
     'coalesce': False,
      'max_instances': 3,
      'misfire_grace_time':10  #10秒的任务超时容错
     }

scheduler = BackgroundScheduler(jobstores=jobstores,executors=executors,job_defaults=job_defaults)

scheduler.start()

def aps_pause():
    """

    :return:
    """
    scheduler.pause_job('interval_task')

def aps_resume():
    scheduler.resume_job('interval_task')

def aps_remove():
    scheduler.remove_job('interval_task')

def getjob(url,id,taskProject,taskName,taskType,taskUrl):


    data = {}
    startTime = int(round(time.time() * 1000))
    res = requests.get(url)
    stopTime = int(round(time.time() * 1000))
    totalTime =str(int(stopTime)- int(startTime))
    if res.status_code != 200:
        data['code'] = 2009
        data['msg'] = '访问失败'
    else:
        data['code'] = 2001
        data['msg'] = {'requestTime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'http_code':200, 'http_resp': res.text,'time':  totalTime + 'ms'}
        kwargs = {}
        kwargs['taskId'] = id
        kwargs['taskProject'] = taskProject
        kwargs['taskName'] = taskName
        kwargs['taskType'] = taskType
        kwargs['taskUrl'] = taskUrl
        kwargs['responseTime'] = totalTime
        kwargs['responseResult'] = res.text
        from mophealth import  models
        models.scanLog.objects.create(**kwargs)


    print(data)

    return  data





def run(taskid,url,intervalTime,opstype):
    """
    :param taskid:
    :param url:
    :param intervalTime:
    :param type: 0-add 1-delete 2-pause 3-resume
    :return:
    """

    from mophealth import models
    res = models.taskList.objects.filter(pk=taskid).values('id','taskProject','taskName','taskType','taskUrl').first()
    if opstype == 0:
        res = scheduler.add_job(func=getjob,args=(url,res['id'],res['taskProject'],res['taskName'],res['taskType'],res['taskUrl'],),trigger='interval', seconds=intervalTime,id=taskid)
        print("这是run方法接收的返回对象s%" ,res)

    if opstype == 1:
        res = scheduler.remove_job(taskid)

    if opstype == 2:
        res = scheduler.pause_job(taskid)

    if opstype == 3:
        res = scheduler.resume_job(taskid)

    if opstype == 4:
        res = scheduler.get_job(taskid)

    print(res)
    #程序开始

    #程序停止
    # time.sleep(30)
    # scheduler.shutdown()
    return  res
