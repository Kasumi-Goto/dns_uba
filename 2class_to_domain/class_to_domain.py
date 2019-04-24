from os import _exit
from fuzzywuzzy import fuzz
import pymysql
import traceback

# 连接配置信息
config = {
    'host': 'localhost',  # mysql服务器
    'port': 3306,  # 端口
    'user': 'root',  # 数据库用户名
    'password': '123456',  # 数据库密码
    'db': 'dns_uba'  # 数据库名
}
classList = []
finalClassList = []
global start
domainList = []
domainClass = []


def read_SqlUnclass(db, sql):
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            domainList.append([row[0], row[1]])
        # print(domainList)
    except:
        print("Error: unable to fetch data")


def read_SqlClass(db, sql):
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            classList.append([row[0], row[1]])
        # print(classList+'\n')
    except:
        print("Error: unable to fetch data\n")


def Classify(s1, s2):
    ratio = fuzz._token_sort(s2, s1, partial=False, force_ascii=True, full_process=True)
    if ratio > 80:
        return True
    else:
        return False


def setClassToDomain():
    for d in domainList:
        for c in classList:
            flag = True
            if Classify(d[0], c[0]):
                d.append(c[1])
                flag = False
                break
        if flag:
            d.append(1024)
    # print(domainList)
    print("\n------------------------")
    print("更新"+str(len(domainList))+"条数据")


if __name__ == '__main__':
    # 连接数据库
    db = pymysql.connect(**config)
    sql = "SELECT web_domainname, id,title FROM userdata WHERE flag=0"
    read_SqlUnclass(db, sql)

    sql = "SELECT url, class FROM website"
    read_SqlClass(db, sql)

    setClassToDomain()
    for i in domainList:
        print(i)
        sql = "UPDATE userdata SET web_class=%s,flag=1 WHERE id=%s"
        para = (i[2], int(i[1]))
        cursor = db.cursor()
        try:
            cursor.execute(sql, para)
            db.commit()
        except:
            traceback.print_exc()
            db.rollback()
            break
        if(i[end]==0):
            sql2 = "INSERT INTO website (url,name,class) VALUES (%s,%s,%s)"
            para = (i[0], int(i[1]),i[2])
            cursor = db.cursor()
            try:
                cursor.execute(sql, para)
                db.commit()
            except:
                traceback.print_exc()
                db.rollback()
                break
    db.close()
    _exit(0)