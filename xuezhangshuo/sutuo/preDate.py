#coding:utf8

# from tornado import database
from ftplib import FTP
import StringIO
import xlrd
import MySQLdb
import re
import signal
import time

import sys,os
# sys.path.insert(0,'path\\to\\your\\python_path')
os.environ['DJANGO_SETTINGS_MODULE']='/Users/scott/dev/projects/web/XueZhangShuo/'

# db = database.Connection("127.0.0.1","sutuo","root","close(f)")
db = MySQLdb.connect("localhost","dxuezang","NBcXudDDyzpERsV2","dxuezang_xzs",charset='utf8')
#convert gb2312 to utf8
def g2u(text):
    try:
        return text.decode('gbk').encode('utf8')
    except:
        return text

classidPatten = re.compile(r'F\d\d\d\d\d\d\d')
sidPatten = re.compile(r'5\d\d\d\d\d\d\d\d\d')
        
def classify(filename,cols):
    classid,name,sid,score,itemid = '','','','',''
    for col in cols:
        try:
            col = int(col)
        except:
            pass
        if (col<=50):
            continue #abnormal score
        if (type(col) ==float or type(col)==int):
            if(col<=100):
                score = str(col)
            elif(sidPatten.match(str(int(col)))):
                sid = str(int(col))
            else:
                itemid = str(int(col))
        elif ((type(col) == unicode) or (type(col) == str)):
            if(classidPatten.match(unicode(col))):
                classid = unicode(col)
            elif(unicode(col)!='' and len(unicode(col))<=5):
                name = unicode(col)
    return g2u(filename),classid.encode('utf8'),name.encode('utf8'),sid,score,itemid



def db_save(filename,cols):
    # print classid.encode('utf8'),name.encode('utf8'),sid,score,itemid
    para = classify(filename,cols)
    if (para[2]!='' or para[3]!=''):
        sqlcmd = """INSERT INTO `dxuezang_xzs`.`sutuo_sutuoitem` (`id`, `filename`, `classID`, `name`, `studentID`, `score`, `itemID`) VALUES (NULL, '%s', '%s', '%s', '%s', '%s', '%s');""" % para
        try:
            db.query(sqlcmd)
        except:
            print sqlcmd

    
def parse(name,filename='tmp.xls'):
    try:
        book = xlrd.open_workbook(filename)
    except xlrd.biffh.XLRDError:
        print "Error:(can't open):",g2u(name)
    else:
        print g2u(name)
        for i in xrange(book.nsheets):
            sh = book.sheet_by_index(i)
            for rx in xrange(1,sh.nrows):
                #try:
                db_save(name, [sh.cell_value(rx,i) for i in range(sh.ncols-1,-1,-1)])
                #except:
#                    print "error line %d" % rx

#    except:
        #print 'error:'+name
#
    
def handler(signum, frame):   
    raise IOError

def loop_name(names):
    for name in names:
        f = open('tmp.xls','wb')
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(5)
        try:
            ftp.retrbinary("RETR "+name,f.write)
            signal.alarm(0)
        except:
            print 'loss:',g2u(name)
            f.close()
            ftp = FTP("202.120.38.171",'seie','zhcp')
            ftp.cwd(pwd)
            names.insert(names.index(name)+1,name)
            continue
        f.close()
        parse(name)


tmpFile = StringIO.StringIO()
#connect
ftp = FTP("202.120.38.171",'seie','zhcp')
count = 0
#change folder
pwd = '/2_下载区/各项分数下载/第1阶段打分下载'.decode('utf8').encode('gbk')
ftp.cwd(pwd)
#get name list
names = ftp.nlst()
count += len(names)
loop_name(names)
pwd = '/2_下载区/各项分数下载/第2阶段增补及修改下载'.decode('utf8').encode('gbk')
ftp.cwd(pwd)
names = ftp.nlst()
count += len(names)
loop_name(names)
#parse('2011.9.10 çŽ‹ç‰§ä¹‹ï¼ˆæ ¡åº†å¿—æ„¿è€…ï¼‰.xlsx'.decode('gbk'),'xq.xls')
print count
ftp.close()