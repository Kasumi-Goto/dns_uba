import codecs
import csv


def countnum(filename):
    count = 0
    for index, line in enumerate(filename):
        count += 1
    return count


def read_csv(filename):
    with codecs.open(filename, 'r') as file:
        r_csv = csv.reader(file)
        data = list(r_csv)
        file.close()
        return data


def save_csv(filename, data):
    with open(filename, 'w+', newline='') as f:
        w_csv = csv.writer(f)
        w_csv.writerows(data)
    f.close()


def transfer_data(res, num):
    for j in range(0, num):
        for i in range(0, 3):
            if res[j][i] == '教育':
                res[j][i] = 1
            if res[j][i] == '购物':
                res[j][i] = 2
            if res[j][i] == '社会':
                res[j][i] = 3
            if res[j][i] == '体育':
                res[j][i] = 4
            if res[j][i] == '科技':
                res[j][i] = 5
            if res[j][i] == '军事':
                res[j][i] = 6
            if res[j][i] == '娱乐':
                res[j][i] = 7
            if res[j][i] == '财经':
                res[j][i] = 8
            if res[j][i] == '生活':
                res[j][i] = 9
            if res[j][i] == '女性健康':
                res[j][i] = 10
            if res[j][i] == '其他':
                res[j][i] = 11
            if res[j][i] == '-1':
                res[j][i] = -1
            if res[j][3] == 'E':
                res[j][3] = 1
            if res[j][3] == 'M':
                res[j][3] = 2
            if res[j][3] == 'D':
                res[j][3] = 3
            if res[j][3] == 'A':
                res[j][3] = 4
    return res


def revert_data(res, num):
    for j in range(0, num):
        if res[j][0] == res[j][1]:
            res[j][1] = res[j][2]
        if res[j][2] == res[j][1] | res[j][2] == res[j][0]:
            res[j][2] = -1
        for i in range(0, 3):
            if res[j][i] == 1:
                res[j][i] = '教育'
            if res[j][i] == 2:
                res[j][i] = '购物'
            if res[j][i] == 3:
                res[j][i] = '社会'
            if res[j][i] == 4:
                res[j][i] = '体育'
            if res[j][i] == 5:
                res[j][i] = '科技'
            if res[j][i] == 6:
                res[j][i] = '军事'
            if res[j][i] == 7:
                res[j][i] = '娱乐'
            if res[j][i] == 8:
                res[j][i] = '财经'
            if res[j][i] == 9:
                res[j][i] = '生活'
            if res[j][i] == 10:
                res[j][i] = '女性健康'
            if res[j][i] == 11:
                res[j][i] = '其他'
        if res[j][3] == 1:
            res[j][3] = 'E'
        if res[j][3] == 2:
            res[j][3] = 'M'
        if res[j][3] == 3:
            res[j][3] = 'D'
        if res[j][3] == 4:
            res[j][3] = 'A'
    return res


def main():
    num = countnum(open('result.csv', 'r'))
    # print(num)
    res = read_csv('result.csv')
    res = transfer_data(res, num)
    save_csv('result_to_number.csv', res)
