# @Author  : kane.zhu
# @Time    : 2020/9/17 11:09
# @Software: PyCharm


from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkbssopenapi.request.v20171214.QueryInstanceBillRequest import QueryInstanceBillRequest
from cmdb import  models as cmdbmodels
from midplatform import  settings
from common import baseconfig
import  json


accesskeyId = baseconfig.getconfig()['accessKey']
accessSecret = baseconfig.getconfig()['accessSecret']

client = AcsClient(accesskeyId,accessSecret, 'cn-hangzhou')
request = QueryInstanceBillRequest()
request.set_accept_format('json')


def getMonthBill(month,pagesize):

    if pagesize not in range(20,301):
        settings.RESULT['code'] = 2009
        settings.RESULT['msg'] = 'fail'
        settings.RESULT['data'] = 'pagesize 请选择[20,300]之间'
        return  settings.RESULT

    request.set_BillingCycle(month)
    request.set_PageSize(1)

    try:
        response = json.loads(str(client.do_action_with_exception(request),encoding='utf-8'))
        getdatacount = int(response['Data']['TotalCount'])
        fetchcount = ( getdatacount // pagesize ) + 2 # 余数向下取整，同时range 左闭右开 所以 +2
        for i in range(1, fetchcount):
            if pagesize > fetchcount:
                pagesize = getdatacount
            insertBillDetail(pagesize,i)

        settings.RESULT['code'] = 2001
        settings.RESULT['msg'] = 'success'
        settings.RESULT['count'] = getdatacount
        return settings.RESULT

    except ClientException as e:
        print(e)

    except ServerException as e:
        print(e)





def insertBillDetail(pagesize,pagenum):
    request.set_PageSize(pagesize)
    request.set_PageNum(pagenum)

    response = json.loads(str(client.do_action_with_exception(request), encoding='utf-8'))
    print(pagesize,pagenum)
    AccountID = response['Data']['AccountID']
    AccountName = response['Data']['AccountName']
    BillingCycle = response['Data']['BillingCycle'] + '-01'
    getdata = response['Data']['Items']['Item']

    billdetaillist=[]
    for i in range(pagesize):
        if getdata[i]['Item'] == 'SubscriptionOrder':
            item = 0
        elif getdata[i]['Item'] == 'PayAsYouGoBill':
            item = 1
        else:
            item = 2

        billdetaillist.append(cmdbmodels.billDetail(accountId=AccountID,
                                                    accountName=AccountName,
                                                    billingCycle=BillingCycle,
                                                    item=item,
                                                    resourceGroup=getdata[i]['ResourceGroup'],
                                                    region=getdata[i]['Region'],
                                                    productDetail=getdata[i]['ProductDetail'],
                                                    productCode=getdata[i]['ProductCode'],
                                                    nickName=getdata[i]['NickName'],
                                                    pretaxAmount=getdata[i]['PretaxAmount']
                                                    ))
        print(billdetaillist)
    cmdbmodels.billDetail.objects.bulk_create(billdetaillist)