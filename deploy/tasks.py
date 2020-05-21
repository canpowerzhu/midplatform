import time
from celery import task
from celery import shared_task


@shared_task
def add(a,b):
  print("这是任务开始")
  print(a+b)
  time.sleep(10)
  print("这是任务结束")
  return a + b