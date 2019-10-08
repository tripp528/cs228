import pickle
import numpy as np
import sys

sys.path.insert(0, '..')
from knn import KNN
knn = KNN()

# files = {"Gordon":[2,3]}
# datasets = []
#
# for person in files:
#     pickle_in_train = open("userData/"+ person +"train.p","rb")
#     pickle_in_train = open("userData/"+ files[i] +"train.p","rb")
#     datasets.append

def CenterData(set):
    for i in range(6):
        set[:,:,i,:] = set[:,:,i,:] - set[:,:,i,:].mean()
    return set


def ReduceData(set):
    #rid of some bones
    set =  np.delete(set,1,1)
    set =  np.delete(set,1,1)

    #  JUST get tips
    set =  np.delete(set,0,2)
    set =  np.delete(set,0,2)
    set =  np.delete(set,0,2)

    return set

def constructDataSet(filename):
    pickle_in = open(filename,"rb")
    dataset = pickle.load(pickle_in)
    pickle_in.close()
    dataset = CenterData(dataset)
    dataset = ReduceData(dataset)
    return dataset

#Childs_test0
Childs_train0 = constructDataSet("userData/Childs_train0.p")
Childs_test0 = constructDataSet("userData/Childs_test0.p")

#Clark_test1
Clark_train1 = constructDataSet("userData/Clark_train1.p")
Clark_test1 = constructDataSet("userData/Clark_test1.p")

Gordon_train2 = constructDataSet("userData/Gordon_train2.p")
Gordon_test2 = constructDataSet("userData/Gordon_test2.p")

Gordon_train3 = constructDataSet("userData/Gordon_train3.p")
Gordon_test3 = constructDataSet("userData/Gordon_test3.p")

Beatty_train4 = constructDataSet("userData/Beatty_train4.p")
Beatty_test4 = constructDataSet("userData/Beatty_test4.p")

Livingston_train5 = constructDataSet("userData/Livingston_train5.p")
Livingston_test5 = constructDataSet("userData/Livingston_test5.p")

#Huang_test6
Huang_train6 = constructDataSet("userData/Huang_train6.p")
Huang_test6 = constructDataSet("userData/Huang_test6.p")

Huang_train7 = constructDataSet("userData/Huang_train7.p")
Huang_test7 = constructDataSet("userData/Huang_test7.p")

Erickson_train8 = constructDataSet("userData/Erickson_train8.p")
Erickson_test8 = constructDataSet("userData/Erickson_test8.p")

Childs_train9 = constructDataSet("userData/Childs_train9.p")
Childs_test9 = constructDataSet("userData/Childs_test9.p")


def ReshapeData(set1,set2,set3,set4,set5,set6,set7,set8, set9, set10):
    totLen = 10000
    X = np.zeros((totLen,5*2*3), dtype='f')
    Y = np.zeros((totLen), dtype='f')

    for row in range(0,1000):
        Y[row] = 0
        Y[row+1000] = 1
        Y[row+2000] = 2
        Y[row+3000] = 3
        Y[row+4000] = 4
        Y[row+5000] = 5
        Y[row+6000] = 6
        Y[row+7000] = 7
        Y[row+8000] = 8
        Y[row+9000] = 9
        col = 0
        for finger in range(0,5):
            for bone in range(0,2):
                for coordinate in range(0,3):
                    X[row,col] = set1[finger,bone,coordinate,row]
                    X[row+1000,col] = set2[finger,bone,coordinate,row]
                    X[row+2000,col] = set3[finger,bone,coordinate,row]
                    X[row+3000,col] = set4[finger,bone,coordinate,row]
                    X[row+4000,col] = set5[finger,bone,coordinate,row]
                    X[row+5000,col] = set6[finger,bone,coordinate,row]
                    X[row+6000,col] = set7[finger,bone,coordinate,row]
                    X[row+7000,col] = set8[finger,bone,coordinate,row]
                    X[row+8000,col] = set9[finger,bone,coordinate,row]
                    X[row+9000,col] = set10[finger,bone,coordinate,row]

                    col += 1

    return X,Y

trainX,trainY = ReshapeData(Childs_train0,Clark_train1,Gordon_train2,Gordon_train3,Beatty_train4, \
                        Livingston_train5,Huang_train6,Huang_train7,Erickson_train8,Childs_train9)

testX,testY = ReshapeData(Childs_test0,Clark_test1,Gordon_test2,Gordon_test3,Beatty_test4, \
                        Livingston_test5,Huang_test6,Huang_test7,Erickson_test8,Childs_test9)

# train
knn.Use_K_Of(15)
knn.Fit(trainX,trainY)

# test

# row = 500
# print(knn.Predict(testX[row,:]))
# print(testY[998])

correctCount = 0
for row in range(0,len(testY)): # 3000
    actualClass = testY[row]
    prediction = knn.Predict(testX[row,:])
    print(row, actualClass, prediction)
    if actualClass == prediction:
        correctCount += 1
print "Percent correct: ", (float(correctCount)/len(testY)) * 100, "%"
print correctCount, "correct"


pickle.dump(knn, open('userData/classifier.p','wb'))
