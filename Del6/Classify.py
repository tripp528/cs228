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

def flipData(set):
    flippedSet = set.copy()
    for i in range(set.shape[3]):
        # print i
        flippedSet[:,:,0,i] = -set[:,:,0,i] # finger, bone, xyzbasetip, gesturenumber
        flippedSet[:,:,3,i] = -set[:,:,3,i] # finger, bone, xyzbasetip, gesturenumber

    return np.concatenate((flippedSet,set),axis=3)

def constructDataSet(filename,train=False):
    pickle_in = open(filename,"rb")
    dataset = pickle.load(pickle_in)
    pickle_in.close()
    dataset = CenterData(dataset)

    if (train == True):
        dataset = flipData(dataset)

    dataset = ReduceData(dataset)
    return dataset

#Childs_test0
Childs_train0 = constructDataSet("userData/Childs_train0.p",train=True)
Childs_test0 = constructDataSet("userData/Childs_test0.p")

#Clark_test1
Clark_train1 = constructDataSet("userData/Clark_train1.p",train=True)
Clark_test1 = constructDataSet("userData/Clark_test1.p")

Gordon_train2 = constructDataSet("userData/Gordon_train2.p",train=True)
Gordon_test2 = constructDataSet("userData/Gordon_test2.p")

Gordon_train3 = constructDataSet("userData/Gordon_train3.p",train=True)
Gordon_test3 = constructDataSet("userData/Gordon_test3.p")

Beatty_train4 = constructDataSet("userData/Beatty_train4.p",train=True)
Beatty_test4 = constructDataSet("userData/Beatty_test4.p")

Livingston_train5 = constructDataSet("userData/Livingston_train5.p",train=True)
Livingston_test5 = constructDataSet("userData/Livingston_test5.p")

#Huang_test6
Huang_train6 = constructDataSet("userData/Huang_train6.p",train=True)
Huang_test6 = constructDataSet("userData/Huang_test6.p")

Huang_train7 = constructDataSet("userData/Huang_train7.p",train=True)
Huang_test7 = constructDataSet("userData/Huang_test7.p")

Erickson_train8 = constructDataSet("userData/Erickson_train8.p",train=True)
Erickson_test8 = constructDataSet("userData/Erickson_test8.p")

Childs_train9 = constructDataSet("userData/Childs_train9.p",train=True)
Childs_test9 = constructDataSet("userData/Childs_test9.p")


def ReshapeData(set1,set2,set3,set4,set5,set6,set7,set8, set9, set10, numSamplesPerSet=1000):
    setList = [set1,set2,set3,set4,set5,set6,set7,set8, set9, set10]
    totLen = 10 * numSamplesPerSet
    X = np.zeros((totLen,5*2*3), dtype='f')
    Y = np.zeros((totLen), dtype='f')

    for row in range(0,numSamplesPerSet):

        for i in range(10):
            Y[row+numSamplesPerSet*i] = i

        col = 0
        for finger in range(0,5):
            for bone in range(0,2):
                for coordinate in range(0,3):

                    for i in  range(10):
                        X[row+numSamplesPerSet*i,col] = setList[i][finger,bone,coordinate,row]

                    col += 1

    return X,Y

trainX,trainY = ReshapeData(Childs_train0,Clark_train1,Gordon_train2,Gordon_train3,Beatty_train4, \
                        Livingston_train5,Huang_train6,Huang_train7,Erickson_train8,Childs_train9,numSamplesPerSet=2000)

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
percentOfTest = .02
for row in range(0,len(testY)):
    if (row % 50 == 0):
        actualClass = testY[row]
        prediction = knn.Predict(testX[row,:])
        print(row, actualClass, prediction)
        if actualClass == prediction:
            correctCount += 1
print "Percent correct: ", (float(correctCount)/(len(testY)*percentOfTest)) * 100, "%"
print correctCount, "correct"


pickle.dump(knn, open('userData/classifier.p','wb'))
