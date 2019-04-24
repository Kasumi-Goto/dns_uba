import random
import socket
import traceback
import chardet
import pymysql
import urllib.request
import re
import urllib.parse
from bs4 import BeautifulSoup

# 连接配置信息
config = {
    'host': 'localhost',  # mysql服务器
    'port': 3306,  # 端口
    'user': 'root',  # 数据库用户名
    'password': '123456',  # 数据库密码
    'db': 'dns_uba'  # 数据库名
}
userList = []
domainList = []
finalData = []
count = 0
flag = []  # 0,0,dname 首尾
fflag = []
socket.setdefaulttimeout(5)  # 设置socket层的超时时间为5秒


def read_Sql(db, sql):
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(domainList) == 0:
            for row in results:
                domainList.append([row[0], row[1]])
        print(domainList)
    except:
        print("Error: unable to fetch data")


def get_html(url):
    my_headers = [
        # 模拟浏览器
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)        Chrome/48.0.2564.116 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)   Chrome/45.0.2454.101 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    ]
    random_header = random.choice(my_headers)
    success = False
    attempts = 1
    urlstr = url
    while not success and attempts < 5:
        try:
            if attempts == 1:
                url = "https://www." + urlstr + "/"
            elif attempts == 2:
                url = "https://" + urlstr + "/"
            elif attempts == 3:
                url = "http://" + urlstr + "/"
            elif attempts == 4:
                url = "http://www." + urlstr + "/"
            elif attempts == 5:
                url = urlstr
            request = urllib.request.Request(url)
            request.add_header('User-Agent', random_header)
            html = urllib.request.urlopen(request, timeout=5)
            success = True
            return html
        except:
            attempts += 1
            if attempts == 5:
                return 0


def isUrlAvilable(html):
    if html == 0:
        return False
    else:
        if html.getcode() == 404:
            return False
        return True


def findTitle(html):
    data1 = html.read()
    chardit1 = chardet.detect(data1)
    if (str(chardit1['encoding']) != 'None'):
        content = data1.decode(chardit1['encoding'], 'ignore').encode(chardit1['encoding'], 'ignore')
        html.close()
        soup = BeautifulSoup(content, "html.parser")
        title = soup.select("title")
        if len(title) != 0:
            if title[0].text.strip() != '':
                return [True, title[0].text.strip()]
            else:
                return [False, '']
        else:
            return [False, '']
    else:
        return [False, '']


def reDomain(url):
    topDomainRex = re.compile(r'((\w+\.\w+\.|\w+\.)\w+$)')
    sm = re.compile(r'^\w+')
    try:
        urll = topDomainRex.findall(url)
        ss = sm.findall(urll[0][0])
        if urll.__len__() == 0:
            return False
        else:
            return [urll[0][0], ss[0]]
    except:
        return False


def hostDomain(url):
    topHostPostfix = (
        '.com', '.la', '.io', '.co', '.info', '.net', '.org', '.me', '.mobi',
        '.us', '.biz', '.xxx', '.ca', '.co.jp', '.com.cn', '.net.cn',
        '.org.cn', '.mx', '.tv', '.ws', '.ag', '.com.ag', '.net.ag',
        '.org.ag', '.am', '.asia', '.at', '.be', '.com.br', '.net.br',
        '.bz', '.com.bz', '.net.bz', '.cc', '.com.co', '.net.co',
        '.nom.co', '.de', '.es', '.com.es', '.nom.es', '.org.es',
        '.eu', '.fm', '.fr', '.gs', '.in', '.co.in', '.firm.in', '.gen.in',
        '.ind.in', '.net.in', '.org.in', '.it', '.jobs', '.jp', '.ms',
        '.com.mx', '.nl', '.nu', '.co.nz', '.net.nz', '.org.nz',
        '.se', '.tc', '.tk', '.tw', '.com.tw', '.idv.tw', '.org.tw',
        '.hk', '.co.uk', '.me.uk', '.org.uk', '.vg', ".com.hk")

    regx = r'[^\.]+(' + '|'.join([h.replace('.', r'\.') for h in topHostPostfix]) + ')$'
    pattern = re.compile(regx, re.IGNORECASE)
    parts = urllib.parse.urlparse("https://" + url)
    host = parts.netloc
    try:
        m = pattern.search(host)
        m.group()
        reg = re.compile('^\w+')
        x = reg.findall(m.group())
        return [m.group(), x[0]]
    except:
        return False


def findDomain():
    finalDomain = []
    for url in domainList:
        result = hostDomain(url[1])
        if result == False:
            result = reDomain(url[1])
        if result == False:
            finalDomain.append('')
        else:
            finalDomain.append([result, url[1], url[0]])
    return finalDomain


def getTwoDimensionListIndex(L, value):
    data = [data for data in L if data[2] == value]
    index = L.index(data[0])
    return index


if __name__ == '__main__':
    try:
        # 连接数据库
        db = pymysql.connect(**config)
        sql = "SELECT DISTINCT ip_saddr FROM package ORDER BY ip_saddr"
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                userList.append(row[0])
            print(userList)
        except:
            print("Error: unable to fetch data")
        for i in range(0, len(userList)):
            print("\n-----User: " + userList[i] + "新增数据如下-----")
            domainList.clear()
            flag.clear()
            fflag.clear()
            sql = "SELECT pid, dns_domainname FROM package WHERE ip_saddr='%s' AND flag=0 " % userList[i]
            read_Sql(db, sql)
            fname = findDomain()  # [[[domain1, domain2], url, number]]
            i = 0
            # 大致分组，按[domain1, domain2]相同分   flag=[[start, end, [domain1, domain2]],[start, end, [domain1, domain2]]]
            for domn in fname:
                if flag.__len__() == 0:  # 0,0,dname 首尾
                    flag.append([domn[0], domn[2]])  # 0,0,dname 首尾
                    i += 1
                elif flag[i - 1][0] == domn[0]:
                    flag[i - 1].append(domn[2])
                else:
                    flag.append([domn[0], domn[2]])
                    i += 1
            fflag = []  # [[start, title,domain2],[start, title, domain2]]
            index = 0  # fflag 组数
            temp = 0
            for f in flag:
                if temp + 1 < index:
                    # print(fflag[temp])
                    temp += 1
                begin = getTwoDimensionListIndex(fname, f[1])
                end = getTwoDimensionListIndex(fname, f[len(f) - 1])
                if index != 0:
                    if fflag[index - 1][1] != begin:  # begin-1 = end
                        fflag[index - 1][1] = begin  # 向上合并
                        if fflag[index - 1][3] == fname[begin][0][1]:  # 向上合并后，新的相邻包顶级域名相同, begin-1 = fname位数
                            fflag[index - 1][1] = end  # 直接合并
                            continue

                for xx in f[1:len(f)]:
                    x = getTwoDimensionListIndex(fname, xx)
                    origin = fname[x][1]  # 原域名
                    top = fname[x][0][0]  # 顶级域名
                    html1 = get_html(origin)  # 原域名html
                    available1 = isUrlAvilable(html1)
                    html2 = get_html(top)  # 顶级域名html
                    available2 = isUrlAvilable(html2)  # 可进
                    if available1:
                        [ok1, title1] = findTitle(html1)  # 有title
                        if ok1:
                            fflag.append([fname[begin][2], fname[end][2], title1, fname[begin][0][1],
                                          fname[begin][0][0]])  # 开始包号，原题目，顶级域名
                            index += 1
                            break
                    if x == end and available2:
                        [ok2, title2] = findTitle(html2)
                        if ok2:
                            fflag.append(
                                [fname[begin][2], fname[end][2], title2, fname[begin][0][1], fname[begin][0][0]])
                            index += 1
            for y in fflag:
                result1 = []
                sql1 = "SELECT pid, request_time, ip_saddr FROM package WHERE pid=%d" % y[0]  # [包号，时间，用户ip]
                try:
                    cursor = db.cursor()
                    cursor.execute(sql1)
                    result1 = cursor.fetchall()
                except:
                    print("Error: unable to fetch data")

                sql3 = "INSERT INTO userdata (start_time, user_ip, web_domainname, web_title, flag) VALUES (%s, %s, %s, %s, 0)"
                para = (result1[0][1], result1[0][2], y[4], y[2])  # [开始时间，用户ip，域名，标题]
                try:
                    cursor = db.cursor()
                    cursor.execute(sql3, para)
                    db.commit()
                    print("插入数据:" + str(result1[0][2]) + " " + str(y[4]))
                    count += 1
                except:
                    db.rollback()
            for x in domainList:
                sql4 = "UPDATE package SET flag=1 WHERE pid=%d" % x[0]
                try:
                    cursor = db.cursor()
                    cursor.execute(sql4)
                    db.commit()
                except:
                    db.rollback()
    except:
        traceback.print_exc()
    finally:
        print("\n------------------------")
        print("插入完成,共" + str(count) + "条新数据")
        try:
            cursor = db.cursor()
            cursor.execute(
                "UPDATE userdata SET user_time = 'D' WHERE DATE_FORMAT(start_time,'%k') BETWEEN 0 AND 5")
            cursor.execute(
                "UPDATE userdata SET user_time = 'M' WHERE DATE_FORMAT(start_time,'%k') BETWEEN 6 AND 11")
            cursor.execute(
                "UPDATE userdata SET user_time = 'A' WHERE DATE_FORMAT(start_time,'%k') BETWEEN 12 AND 17")
            cursor.execute(
                "UPDATE userdata SET user_time = 'E' WHERE DATE_FORMAT(start_time,'%k') BETWEEN 18 AND 23")
            db.commit()
            print("时间转换完成")
        except:
            db.rollback()
            print("错误")
        db.close()
