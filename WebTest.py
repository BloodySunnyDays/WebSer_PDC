# -*- coding:utf-8 -*-
__author__ = 'Djj'


import datetime
import os,sys
import json



def datetime_offset_by_month(datetime1, n = 1):
    one_day = datetime.timedelta(days = 1)
    q,r = divmod(datetime1.month + n, 12)
    datetime2 = datetime.datetime(
        datetime1.year + q, r + 1, 1) - one_day
    if datetime1.month != (datetime1 + one_day).month:
        return datetime2
    if datetime1.day >= datetime2.day:
        return datetime2
    return datetime2.replace(day = datetime1.day)

from suds.client import Client
#
#

# print time.time()
# strd = test.service.FindUser(u'黄鑫军','330719198309053911')
# print time.time()
#
# print strd

# dtstr = '2014-02-14 21:32:12'
#
# print datetime.datetime.strptime(dtstr, "%Y-%m-%d %H:%M:%S").date()
# print datetime.date.today()
#
# print datetime.datetime.strptime(dtstr, "%Y-%m-%d %H:%M:%S").date() < datetime.date.today()
# print datetime.datetime.strptime(str(datetime.datetime.today()), "%Y-%m-%d %H:%M:%S")

# print datetime_offset_by_month(datetime.date.today(),12)
# print datetime.datetime.strptime(str(datetime.date.today()), "%Y-%m-%d %H:%M:%S") < datetime.datetime.strptime(dtstr, "%Y-%m-%d %H:%M:%S")


WebIP = '192.168.0.44'
# WebIP = '218.4.64.93'
# print  test.service.AddMoney('330719198309053911','9911','01')
# print "11 " + repr(WebIP) +" 22"
#
print datetime.datetime.now()
test=Client('http://'+WebIP+':8733/SOAP/?wsdl')
print datetime.datetime.now()
# print test.service.FindUser(u'黄鑫军','330719198309053911')
# print test.service.FindUser(u'严怡','320524196212084008')

sjson = test.service.GetTicket()
#
print sjson

sjson = u'''{"billno":"100101037","clientcode":"00000000","clientname":"上海携程国际旅行社有限公司",
"areacode":"001","ticketcount":2,"paysum":100.00,"username":"龙威","telno":"18980783123","certno":"510106198908242510",
"Billdetail":[{"ticketmodelname": "景区联票", "ticketmodelcode": "1011","price":40.0,"count":1,"startdate":"2016-07-03","enddate":"2016-07-07"},
{"ticketmodelname": "景区门票", "ticketmodelcode": "1014","price":60.0,"count":1,"startdate":"2016-07-03","enddate":"2016-07-07"}]}'''
# sjson = '{"billno":"100101011","clientcode":"00000000","clientname":"\xe4\xb8\x8a\xe6\xb5\xb7\xe6\x90\xba\xe7\xa8\x8b\xe5\x9b\xbd\xe9\x99\x85\xe6\x97\x85\xe8\xa1\x8c\xe7\xa4\xbe\xe6\x9c\x89\xe9\x99\x90\xe5\x85\xac\xe5\x8f\xb8","areacode":"001","ticketcount":2,"paysum":100.00,"username":"\xe9\xbe\x99\xe5\xa8\x81","telno":"18980783123","certno":"510106198908242510","Billdetail":[{"ticketmodelname": "\xe6\x99\xaf\xe5\x8c\xba\xe8\x81\x94\xe7\xa5\xa8", "ticketmodelcode": "1012"}, {"ticketmodelname": "\xe6\x99\xaf\xe5\x8c\xba\xe9\x97\xa8\xe7\xa5\xa8", "ticketmodelcode": "1013"}]}'

# sjson = '11'
# print type(sjson)
# print repr(sjson)


# test.service.AddBill(repr(sjson))

# print test.service.AddBill(sjson)

# print test.service.BillAreOrder('201512240015918003X')

# obj_json =  json.loads(sjson)



# sbillno = obj_json['billno']
#
# print sbillno
#
# print obj_json
#
# print type(obj_json)
#
# print obj_json['billno']
# print obj_json['ticketcount']
# print obj_json['paysum']
#
# print type(obj_json['billno'])
#
# print type(obj_json['Billdetail'])
#
# for name in obj_json['Billdetail']:
#     print name['ticketmodelname'],name['ticketmodelcode']
#
# print datetime.datetime.now()

# dd = [{'ticket':'1','ticketname':'aaa'},{'ticket':'2','ticketname':'bbbb'}]
#
# print dd[0]['ticket']
#
# for i in dd:
#     print  i['ticketname']