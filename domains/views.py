from django.shortcuts import render, HttpResponse
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from domains import models
import json
import requests, request
from aliyunsdkcore.client import AcsClient
from aliyunsdkdomain.request.v20180129.QueryDomainListRequest import QueryDomainListRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest

#### 域名接口
s = requests.session()


def accountlist(request):
    limit = int(request.GET.get('limit', default='10'))
    page = int(request.GET.get('page', default='1'))
    status = request.GET.get('status')
    remark = request.GET.get('remark')
    # print("cid is %s, remark is %s" % (cid, remark))
    if page == 1:
        start = 0
        stop = limit
    else:
        start = (page - 1) * limit
        stop = limit * page
    kwargs = {
        ##d
    }
    if status != None:
        kwargs['status'] = status

    if remark != None:
        kwargs['remark'] = remark
    if remark != None and status != None:
        kwargs['remark'] = remark
        kwargs['status'] = status
    if remark == None and status == None:
        res = models.Domainaccount.objects.all()[start:stop].values()
    else:
        res = models.Domainaccount.objects.filter(**kwargs).values()

    count = res.count()

    if len(res) > 0:
        datalist = list(res)


        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'
        settings.RESULT['count'] = count
        settings.RESULT['data'] = datalist

    else:
        settings.RESULT['msg'] = "fail"
    return JsonResponse(settings.RESULT)


def domaininfo(request):
    limit = int(request.GET.get('limit', default='10'))
    page = int(request.GET.get('page', default='1'))

    project = request.GET.get('project')
    domain_name = request.GET.get('domain_name')

    if page == 1:
        start = 0
        stop = limit
    else:
        start = (page - 1) * limit
        stop = limit * page
    kwargs = {
        ##d
    }
    if project != None:
        kwargs['project'] = project

    if domain_name != None:
        kwargs['domain_name'] = domain_name

    if domain_name != None and project != None:
        kwargs['domain_name'] = domain_name
        kwargs['project'] = project

    if domain_name == None and project == None:
        res = models.Domaininfo.objects.all().values()
    else:
        res = models.Domaininfo.objects.filter(**kwargs).values()

    count = res.count()

    if len(res) > 0:
        datalist = list(res)
        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'
        settings.RESULT['count'] = count
        settings.RESULT['data'] = datalist
        return JsonResponse(settings.RESULT)
    else:
        settings.RESULT['msg'] = "fail"
        print(settings.RESULT)
    return HttpResponse("fail")


def domainsync(request):
    """
    同步各个账户的域名列表接口
    http://127.0.0.1:88/domains/domainsync/?account=adam.king
    """
    api_url = settings.DOMAIN['getdomian_api_url']
    account = request.GET.get('account')
    res = models.Domainaccount.objects.filter(username=account).first()
    token = res.token.strip()
    result = {}
    result['username'] = account
    result['token'] = token
    ## 使用JsonResponse 返回字典，直接响应json

    s.auth = (account, token)
    res = s.get(url=api_url)
    if res.status_code == 200:
        domainresult = res.content.decode('utf-8')
        if 'domains' in domainresult:
            data = json.loads(domainresult)['domains']
            ###利用bulk_create进行批量插入
            domain_obj_list = []
            for i in range(len(data)):
                print(">>>>>> %s" % data[i]['domainName'])
                recordinfo(s, api_url, data[i]['domainName'], account)

                if 'autorenewEnabled' not in data[i]:
                    # if 	data[i].has_key('autorenewEnabled'): ###python3 已经删除了has_key方法
                    data[i]['autorenewEnabled'] = False
                if 'locked' not in data[i]:
                    data[i]['locked'] = False
                domain_obj_list.append(
                    models.Domainlist(name_account=account,
                                      domainName=data[i]['domainName'],
                                      locked=data[i]['locked'],
                                      autorenewEnabled=data[i]['autorenewEnabled'],
                                      expireDate=data[i]['expireDate'].split('T')[0],
                                      createDate=data[i]['createDate'].split('T')[0])
                )
        else:
            result['msg'] = 'no domain'
            return JsonResponse(result)
        models.Domainlist.objects.filter(name_account=account).delete()
        models.Domainlist.objects.bulk_create(domain_obj_list)
        result['data'] = data
    else:
        print("request failed")
    return JsonResponse(result)


def recordinfo(s, api_url, domian, username):
    """
    内部使用的同步二级域名至数据库
    """
    # record_api_url = 'https://api.name.com/v4/domains/ztianr.com/records'
    record_obj_list = []
    record_api_url = api_url + '/' + domian + '/records'
    # username = 'peterlin.zhou'
    # token = 'd07d86b09c8b9587414f9b909480aa1e4456b981'
    # s.auth = (username, token)
    record_res = s.get(url=record_api_url)
    if record_res.status_code == 200:
        result = record_res.content.decode('utf-8')
        result = json.loads(result)
        if result:
            for i in range(len(result['records'])):
                print(result['records'][i])
                record_obj_list.append(
                    models.Domaininfo(name_account=username,
                                      register_website='www.name.com',
                                      domain_name=result['records'][i]['domainName'],
                                      fqdn=result['records'][i]['fqdn'],
                                      type=result['records'][i]['type'],
                                      answer=result['records'][i]['answer']
                                      )
                )
            models.Domaininfo.objects.filter(domain_name=result['records'][i]['domainName']).delete()
            models.Domaininfo.objects.bulk_create(record_obj_list)
    return HttpResponse('ok')


def modifydomianinfo(request):
    """
    修改二级域名的所属项目以及备注
    """
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        msg = json.loads(data)
        domainid = msg['id']
        project = msg['project']
        remark = msg['remark']
        models.Domaininfo.objects.filter(pk=domainid).update(project=project, remark=remark)
        front_respone = {'code': 2001, 'msg': 'success'}
        return JsonResponse(front_respone)


def domainlist(request):
    """
    域名列表的接口
    """

    limit = int(request.GET.get('limit', default='10'))
    page = int(request.GET.get('page', default='1'))
    if page == 1:
        start = 0
        stop = limit
    else:
        start = (page - 1) * limit
        stop = limit * page

    res = models.Domainlist.objects.all().order_by('expireDate').values()[start:stop]
    count = models.Domainlist.objects.all().count()

    if len(res) > 0:
        datalist = list(res)

        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'
        settings.RESULT['count'] = count
        settings.RESULT['data'] = datalist
        return JsonResponse(settings.RESULT)
        # data = json.dumps(settings.RESULT)
        # return HttpResponse(data)
    else:
        settings.RESULT['msg'] = "fail"
        print(settings.RESULT)
    return HttpResponse("fail")


def modifyaccount(request):
    """
    修改域名账户的使用状态
    """
    if request.method == 'POST':
        res = json.loads(request.body.decode('utf-8'))
        print(res, type(res))
        id = int(res['account_id'])
        if res['status']:
            status = '1'
        else:
            status = '0'

        is_ok = models.Domainaccount.objects.filter(pk=id).update(status=status)
        front_respone = {'code': 2001, 'msg': None}

        if is_ok == 1:
            front_respone['msg'] = 'success'
        else:
            front_respone['code'] = 2002
            front_respone['msg'] = 'fail'

        return JsonResponse(front_respone)


def aliyundomainsync(request):
    """
    阿里云的万网域名接口
    get 请求 参数account
    """
    username = request.GET.get('account')
    accessKeyId = models.Domainaccount.objects.get(username=username).token_name
    accessSecret = models.Domainaccount.objects.get(username=username).account_code
    client = AcsClient(accessKeyId, accessSecret, 'cn-hangzhou')

    request = QueryDomainListRequest()
    request.set_accept_format('json')
    request.set_PageNum(1)
    request.set_PageSize(50)

    response = client.do_action_with_exception(request)
    data = json.loads(response.decode('utf-8'))['Data']['Domain']
    domainlist = []
    for i in range(len(data)):
        aliyunDomainRecord(data[i]['DomainName'], client, username)

        domainlist.append(models.Domainlist(
            name_account=username,
            domainName=data[i]['DomainName'],
            locked=0,
            autorenewEnabled=0,
            expireDate=data[i]['ExpirationDate'].split(' ')[0],
            createDate=data[i]['RegistrationDate'].split(' ')[0]

        ))
    models.Domainlist.objects.filter(name_account=username).delete()
    models.Domainlist.objects.bulk_create(domainlist)
    return HttpResponse('ok')


def aliyunDomainRecord(domain, client, username):
    """
    阿里云万网域名接口 内部调用域名解析记录详情
    """
    request = DescribeDomainRecordsRequest()
    request.set_accept_format('json')

    request.set_DomainName(domain)

    response = client.do_action_with_exception(request).decode('utf-8')
    records = json.loads(response)['DomainRecords']['Record']
    domaininfolist = []
    if len(records) > 0:

        for i in range(len(records)):
            domaininfolist.append(models.Domaininfo(
                register_website='www.aliyun.com',
                name_account=username,
                domain_name=records[i]['DomainName'],
                fqdn=records[i]['RR'] + '.' + records[i]['DomainName'],
                type=records[i]['Type'],
                answer=records[i]['Value']
            ))
        print(domaininfolist)
        models.Domaininfo.objects.filter(name_account=username, domain_name=records[i]['DomainName']).delete()
        models.Domaininfo.objects.bulk_create(domaininfolist)
