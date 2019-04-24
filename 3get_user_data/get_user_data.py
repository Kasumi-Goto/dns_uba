import csv

import pymysql

# 连接配置信息
config = {
    'host': 'localhost',  # mysql服务器
    'port': 3306,  # 端口
    'user': 'root',  # 数据库用户名
    'password': '123456',  # 数据库密码
    'db': 'dns_uba'  # 数据库名
}
data = []
res = []


def getdata():
    db = pymysql.connect(**config)
    sql = """
            SELECT type.*, time.user_time
            FROM 
                (SELECT *
                 FROM tmptime a
                 WHERE 1>(
                        SELECT COUNT(*) 
                        FROM tmptime
                        WHERE user_ip=a.user_ip and counts>a.counts)
                        ORDER BY a.user_ip, a.counts desc) time JOIN
                (SELECT t.user_ip, SUM(教育),SUM(购物),SUM(社会),SUM(体育),SUM(科技),SUM(军事),SUM(娱乐),SUM(财经),SUM(生活),SUM(女性健康),SUM(其他)
                 FROM 
                    (SELECT user.user_ip, user.web_domainname, class.* 
                     FROM userdata user 
                     LEFT JOIN final_class class
                     ON user.web_class=class.id) t
                     GROUP BY user_ip) type
            ON time.user_ip = type.user_ip;
        """
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            data.append(row)
    except:
        print("Error: unable to fetch data")


def save_csv(filename, data):
    with open(filename, 'w+', newline='') as f:
        w_csv = csv.writer(f)
        w_csv.writerows(data)
    f.close()


if __name__ == '__main__':
    db = pymysql.connect(**config)
    sql = """
                CREATE TABLE tmptime AS
                    (SELECT start_time AS start_time, user_ip AS user_ip, user_time AS user_time, COUNT(user_time) AS counts 
                        FROM userdata
                        GROUP BY user_ip, user_time ORDER BY user_ip, COUNT(user_time) DESC);"""
    cursor = db.cursor()
    try:
        cursor.execute(sql)
    except:
        print("Error")

    getdata()
    for i in data:
        arr = []
        tmpdict = {}
        type = ['教育', '购物', '社会', '体育', '科技', '军事', '娱乐', '财经', '生活', '女性健康', '其他']
        if i[1] != 0:
            tmpdict = {type[0]: int(i[1])}
        for x in range(1, 11):
            if i[x + 1] != 0:
                tmpdict.update({type[x]: int(i[x + 1])})
        keys = sorted(tmpdict.items(), key=lambda k: k[1], reverse=True)
        if len(keys) == 1:
            res.append([i[0], keys[0][0], -1, -1, i[12]])
        elif len(keys) == 2:
            res.append([i[0], keys[0][0], keys[1][0], -1, i[12]])
        elif len(keys) >= 3:
            res.append([i[0], keys[0][0], keys[1][0], keys[2][0], i[12]])
    save_csv("result.csv", res)
    print("\n------------------------")
    print("用户常用网站类型get")

    sql = "DROP TABLE tmptime"
    cursor = db.cursor()
    try:
        cursor.execute(sql)
    except:
        print("Error")
