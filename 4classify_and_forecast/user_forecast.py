from sklearn.externals import joblib
from sklearn.datasets import load_iris
import RF1.RF1 as a
import list.list as lt

newres = []
num = lt.countnum(open('result.csv', 'r'))
trees2 = joblib.load("train_model.m")
clf = joblib.load("train_model.m")
test = lt.transfer_data(lt.read_csv('result.csv'), num)
predictions = [a.bagging_predict(clf, row) for row in test]
for i in range(0, num):
    test[i].append(predictions[i])
    print(test[i])
newres = lt.revert_data(test, num)
lt.save_csv('user_forecast.csv', newres)
