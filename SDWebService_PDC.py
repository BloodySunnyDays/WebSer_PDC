# -*- coding:utf-8 -*-


__author__ = 'Djj'

import sys
import os
import ConfigParser
import json
import oracle_db
import datetime



import soaplib
from soaplib.core.util.wsgi_wrapper import run_twisted #发布服务
from soaplib.core.server import wsgi
from soaplib.core.service import DefinitionBase  #所有服务类必须继承该类
from soaplib.core.service import soap
from soaplib.core.model.primitive import Integer,String
from soaplib.core.model.clazz import Array #声明要使用的类型
from soaplib.core.model.clazz import ClassModel  #若服务返回类，该返回类必须是该类的子类

# 准备数据
def cur_file_dir():
     path = sys.path[0]
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)

sDir = cur_file_dir() + '\\Config.ini'
config = ConfigParser.ConfigParser()
config.read(sDir)

# 获取路径
def cur_file_dir():
     path = sys.path[0]
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)

sIP        = config.get("conn", "IP")
sPort      = config.get("conn", "Port")
sDateBase  = config.get('conn', 'DateBase')
sUser      = config.get('conn', 'User')
# sPassw     = config.get('conn', 'Paswd')
sWebSerIp  = config.get('conn', 'WebSerIp')



class WorldServiceIntf(DefinitionBase):  #this is a web service
    @soap(_returns=String)    #声明一个服务，标识方法的参数以及返回值
    def GetTicket(self):
        sSQL = "select ticketmodelcode,ticketmodelname from sys_ticketmodel "

        fname = 'log'+str(datetime.date.today()) + '.txt'
        sDir = cur_file_dir() + '\\log\\'+fname

        with open(sDir, 'a') as f:
            f.write(sSQL + '\n')

        tickets =  oracle_db.select(sSQL)

        if len(tickets) ==0:
            return 'No Date'

        for ticket in tickets:
            ticketname = ticket['ticketmodelname'].encode('raw_unicode_escape')
            ticketname = ticketname.decode('gbk')
            ticket['ticketmodelname'] = ticketname

        data_string = json.dumps(tickets, ensure_ascii=False)
        return data_string

    #判断是否已经出票
    @soap(String,_returns=String)
    def BillAreOrder(self,billno):

        fname = 'log'+str(datetime.date.today()) + '.txt'
        sDir = cur_file_dir() + '\\log\\'+fname

        sbillno = str(billno.encode('gbk'))

        sSQL = 'select count(1) as count from web_billmain where billno = ? '
        with open(sDir, 'a') as f:
            f.write(sSQL + ':' +sbillno +'\n')

        Fexist =  oracle_db.select(sSQL,sbillno)

        if Fexist[0]['COUNT'] != 0:
            return 'BillNo already Order a ticket !'
        return '0'


    # 传人json
    @soap(String,_returns=String)
    def AddBill(self,sjson):

        sjson = sjson.encode('raw_unicode_escape').decode('gbk')
        fname = 'log'+str(datetime.date.today()) + '.txt'
        sDir = cur_file_dir() + '\\log\\'+fname

        with open(sDir, 'a') as f:
            f.write(sjson + '\n')



        obj_json =  json.loads(sjson)

        sbillno = obj_json['billno']

        # 判断订单有没有重复
        sSQL = 'select count(1) as count from web_billmain where billno = ? '



        with open(sDir, 'a') as f:
            f.write(sSQL + ':' +sbillno +'\n')

        Fexist =  oracle_db.select(sSQL,sbillno)

        if Fexist[0]['COUNT'] != 0:
            return 'BillNo already exists!'


        # 插入主表,明细表，检票表
        # 封装在一个事务
        @oracle_db.with_transaction
        def add_bill(jsonobj):

            strbillno = jsonobj['billno']
            sclientcode = jsonobj['clientcode']
            sclientname = jsonobj['clientname']
            sareacode = jsonobj['areacode']
            nticketcount = jsonobj['ticketcount']
            cpaysum = jsonobj['paysum']
            susername = jsonobj['username']
            stelno = jsonobj['telno']
            scertno = jsonobj['certno']

            # 主表
            sSQL = "insert into web_billmain(id,billno,billoutno,traveldate,billdate,billstatus,billtype,webbillstatus,"\
                    "clientCode,clientname,areacode,ticketcount,paysum,paytype,payflag,username,"\
                    "telno,certtype,certno,create_time,modified_time,deleted) "\
                    "values (seq_webbillid.nextval,'" + strbillno + "','"+ strbillno +"',trunc(sysdate),sysdate,0,'pdc','valid',"\
                    "'"+sclientcode +"','" + sclientname + "','" + sareacode + "'," + str(nticketcount) + "," + str(cpaysum) + ","\
                    "'07',1, '"+susername+"','" +stelno +"','01','"+ scertno + "',sysdate,sysdate,0)"

            with open(sDir, 'a') as f:
                f.write(str(sSQL.encode('gbk'))  +'\n')

            oracle_db.update(str(sSQL.encode('gbk')))


            # 明细
            for name in jsonobj['Billdetail']:
                sticketmodelname,sticketmodelcode = name['ticketmodelname'],name['ticketmodelcode']
                cprice,ncount = name['price'],name['count']
                ctotal = cprice * ncount
                startdate,enddate = name['startdate'],name['enddate']


                sSQLDetail = "insert into web_billdetail(id,billno,billdate,traveldatetime,invalidatetime,billstatus,webbillstatus,"\
                             "billtype,tickettype,ticketmodelcode,ticketmodelname,ticketcount,ticketprice,paysum,payflag,create_time,"\
                             "deleted) values(seq_webbillid.nextval,'" +strbillno + "',sysdate,trunc(sysdate),date '"+enddate+"',0,'valid',"\
                             "'pdc',100001,'"+sticketmodelcode+"','"+sticketmodelname+"','"+str(ncount)+"','"+str(cprice)+"','"+str(ctotal)+"',1,sysdate,0)"

                with open(sDir, 'a') as f:
                    f.write(str(sSQLDetail.encode('gbk')) +'\n')

                oracle_db.update(str(sSQLDetail.encode('gbk')))


                #判断
                sSQLTmp = "select count(1) as count from sys_ticketmodel where ticketmodelcode = ? "

                Fexist =  oracle_db.select(sSQLTmp,sticketmodelcode)


                if Fexist[0]['COUNT'] == 0:
                    oracle_db._db_ctx.connection.rollback()
                    return '没有对应票型! will cause rollback...'


                #检票表
                sSQLCk = "select b.* from sys_ticketmodeldetail  a left join sys_ticket b on a.ticketid = b.id "\
                         "where ticketmodelcode = ? "

                ticketlist = oracle_db.select(sSQLCk,sticketmodelcode)
                if len(ticketlist) ==0:
                    oracle_db._db_ctx.connection.rollback()
                    return'没有对应单票! will cause rollback...'

                for aticket in ticketlist:
                    ticketcode = aticket['TICKETCODE']
                    ticketname = aticket['TICKETFULLNAME'].decode('gbk')
                    ticketprice = aticket['PRICE']
                    ticketkind  = aticket['TICKETKIND']
                    seasontype  = aticket['SEASONTYPE']
                    parkcode    = aticket['PARKCODE']
                    # 准备条码
                    # 客户代码
                    sSQLTmp = ' select trim(a.paramvalue) as khdm from sys_param a where a.paramcode = 0004'
                    kh = oracle_db.select(sSQLTmp)
                    khdm = kh[0]['KHDM']
                    sSQLTmp = "select lpad(Seq_BarCode.nextVal,8,'0') as seqbarcode from dual "
                    Seq_BarCode = oracle_db.select(sSQLTmp)
                    sq_barcode = Seq_BarCode[0]['SEQBARCODE']

                    barcode = 'WT' + str(datetime.datetime.now().strftime('%Y%m%d')) + khdm + sq_barcode


                    sSQLCk = "insert into web_checkdetail(id,billno,billdate,billtype,barcode,certno,clienttype,clientname,parkcode, "\
                             "parkprice,ticketcode,ticketname,ticketmodel,ticketmodelname,ticketmodelprice,tickettype,ticketkindcode,"\
                             "seasontype,usercount,useflag,leftcount,begindate,invalidate) values ( "\
                             "seq_webbillid.nextval,'" +strbillno + "',sysdate,'pdc','" +barcode + "','" +scertno + "','02', "\
                             "'" +sclientname + "','" +parkcode + "','" +str(ticketprice) + "','" +ticketcode + "','" +ticketname + "', '"\
                             +sticketmodelcode + "','" +sticketmodelname + "','" +str(cprice) + "',100001,'" + ticketkind + "', '"\
                             +str(seasontype) + "','" + str(ncount) + "',0,'" + str(ncount) + "',date '"+startdate+"',date '"+enddate+"')"

                    with open(sDir, 'a') as f:
                        f.write(str(sSQLCk.encode('gbk')) +'\n')

                    oracle_db.update(str(sSQLCk.encode('gbk')))


            return 'success'


        try:
            res = add_bill(obj_json)
        except ImportError:
            return '数据提交失败'

        return res






#网络SOAP 处理提高效率
def Run_Tws():
    soap_app=soaplib.core.Application([WorldServiceIntf], 'tns')
    wsgi_app=wsgi.Application(soap_app)
    # print 'listening on 218.4.64.93:8092'
    # print 'wsdl is at: http://218.4.64.93:8092/SOAP/?wsdl'
    run_twisted( ( (wsgi_app, "SOAP"),), int(sPort))


def Run_Ser():
    try:
        from wsgiref.simple_server import make_server
        soap_application = soaplib.core.Application([WorldServiceIntf], 'tns')
        wsgi_application = wsgi.Application(soap_application)
        server = make_server(sWebSerIp, int(sPort), wsgi_application)
        server.serve_forever()

    except ImportError:
        print 'WebService error'
        raw_input()


def GetDBConnet():
    try:
        print u'version 160801 普达措'
        print sUser
        print sDateBase
        print 'datebaseIP:',sIP
        print sWebSerIp,':',sPort
        sPassw = raw_input('password:')
        os.system('cls')

        oracle_db.create_engine(user=sUser, password=sPassw, database=sDateBase, host=sIP)
        print u'version 160801 普达措'
        print sUser
        print sDateBase
        print 'datebaseIP:',sIP
        print sWebSerIp,':',sPort
        print u'保持窗口不要关闭！。。。'
        return True
    except ImportError:
        print 'DateBaseServer error'
        raw_input()


if GetDBConnet():
    Run_Tws()
