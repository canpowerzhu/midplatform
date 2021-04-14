
from django.http import JsonResponse
from midplatform import  settings
import json
from ansibletower import  models
from django.db.models import F
def configinfo(request):
     if request.method == 'GET' or request.method == 'get':
         parentId = request.GET.get('nodeId')

         res = list(models.configinfo.objects.filter(parentId=parentId).values())
         settings.RESULT['code'] = 2001
         settings.RESULT['msg'] = 'success'
         settings.RESULT['count'] = len(res)
         settings.RESULT['data'] = list(res)
         return JsonResponse(settings.RESULT)

     if request.method == 'PUT' or request.method == 'POST':
         res = json.loads(request.body.decode('utf-8'))
         print(res)
         object,created=models.configinfo.objects.update_or_create(versioncode=res['versioncode'],defaults=res)
         print(object,created)
         if created:
             settings.RESULT['data'] = '新增成功'
         else:
             settings.RESULT['data'] = '修改成功'
         settings.RESULT['code'] = 2001
         settings.RESULT['msg'] = 'success'
         return JsonResponse(settings.RESULT)





def configtree(request):
    if request.method == 'GET' or request.method == 'get':
        action = int(request.GET.get('action'))
        if action == 0:
            res = list(models.configTree.objects.filter(parentId=0).values())
            for i in range(len(res)):
                alltempres = models.configTree.objects.filter(parentId=res[i]['id']).values()
                res[i]['children'] = list(alltempres)
        if action == 1:
            res = list(models.configTree.objects.filter(parentId=0).annotate(title=F('name'), key=F('hierarchy')).values('id','title','key'))
            for i in range(len(res)):
                tempres = models.configTree.objects.filter(parentId=res[i]['id']).annotate(title=F('name'),key=F('hierarchy')).values('id','title','key')
                for j in range(len(tempres)):
                    tempres[j]['isLeaf'] = True
                res[i]['children'] = list(tempres)

        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'
        settings.RESULT['count'] = len(res)
        settings.RESULT['data'] = list(res)
        return JsonResponse(settings.RESULT)

    if request.method == 'POST' or request.method == 'POST':
        res = json.loads(request.body.decode('utf-8'))

        #拼接hierarchy 利用同一parentId count +1 进行追加
        count = models.configTree.objects.filter(parentId=res['parentId']).count()
        newhierarchy = str(res['parentId']) + '-' + str(count+1)
        res['hierarchy'] = newhierarchy
        models.configTree.objects.create(**res)
        settings.RESULT['data'] = '新增成功'
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'
        return JsonResponse(settings.RESULT)


    if request.method == 'PUT' or request.method == 'put':
        res = json.loads(request.body.decode('utf-8'))

        models.configTree.objects.filter(id=res['id']).update(description=res['description'],name=res['name'],sort=res['sort'])
        settings.RESULT['data'] = '编辑成功'
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'
        return JsonResponse(settings.RESULT)


    if request.method == 'DELETE' or request.method == 'delete':
        id = request.GET.get('id')
        print(id)
        models.configTree.objects.filter(pk=id).delete()
        # models.configTree.objects.filter(id=res['id']).update(description=res['description'],name=res['name'],sort=res['sort'])
        settings.RESULT['data'] = '编辑成功'
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'
        return JsonResponse(settings.RESULT)
