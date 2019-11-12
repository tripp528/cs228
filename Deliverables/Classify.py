import pickle
import numpy as np

from knn import KNN
knn = KNN()
samplesPerSet = 2000
numSets = 2

pickle_in_train2 = open("userData/train2.p","rb")
train2 = pickle.load(pickle_in_train2)
pickle_in_train2.close()

pickle_in_train3 = open("userData/train3.p","rb")
train3 = pickle.load(pickle_in_train3)
pickle_in_train3.close()

pickle_in_test2 = open("userData/test2.p","rb")
test2 = pickle.load(pickle_in_test2)
pickle_in_test2.close()

pickle_in_test3 = open("userData/test3.p","rb")
test3 = pickle.load(pickle_in_test3)
pickle_in_test3.close()

def flipData(set):
    flippedSet = set.copy()
    for i in range(set.shape[3]):
        # print i
        flippedSet[:,:,0,i] = -set[:,:,0,i] # finger, bone, xyzbasetip, gesturenumber
        flippedSet[:,:,3,i] = -set[:,:,3,i] # finger, bone, xyzbasetip, gesturenumber

    return np.concatenate((flippedSet,set),axis=3)

def CenterData(set):
    for i in range(6):
        set[:,:,i,:] = set[:,:,i,:] - set[:,:,i,:].mean()
    return set

train2 = flipData(CenterData(train2))
train3 = flipData(CenterData(train3))
test2 = flipData(CenterData(test2))
test3 = flipData(CenterData(test3))

# Draw them
from Reader import READER
reader = READER()
print("train2")
for gestureNumber in range(samplesPerSet):
    if(gestureNumber % 100 == 0):
        gesture = train2[:,:,:,gestureNumber]
        reader.Draw_Gesture(gesture)
print("test2")
for gestureNumber in range(samplesPerSet):
    if(gestureNumber % 100 == 0):
        gesture = test2[:,:,:,gestureNumber]
        reader.Draw_Gesture(gesture)
print("train3")
for gestureNumber in range(samplesPerSet):
    if(gestureNumber % 100 == 0):
        gesture = train3[:,:,:,gestureNumber]
        reader.Draw_Gesture(gesture)
print("test3")
for gestureNumber in range(samplesPerSet):
    if(gestureNumber % 100 == 0):
        gesture = test3[:,:,:,gestureNumber]
        reader.Draw_Gesture(gesture)

def ReduceData(set):
    #rid of some bones
    set =  np.delete(set,1,1)
    set =  np.delete(set,1,1)

    #  JUST get tips
    set =  np.delete(set,0,2)
    set =  np.delete(set,0,2)
    set =  np.delete(set,0,2)

    return set

train2 = ReduceData(train2)
train3 = ReduceData(train3)
test2 = ReduceData(test2)
test3 = ReduceData(test3)

def ReshapeData(set1,set2):
    X = np.zeros((samplesPerSet * numSets,5*2*3), dtype='f')
    Y = np.zeros((samplesPerSet * numSets), dtype='f')
    for row in range(0,samplesPerSet):
        Y[row] = 2
        Y[row+samplesPerSet*1] = 3
        col = 0
        for finger in range(0,5):
            for bone in range(0,2):
                for coordinate in range(0,3):
                    X[row,col] = set1[finger,bone,coordinate,row]
                    X[row+samplesPerSet,col] = set2[finger,bone,coordinate,row]
                    col += 1
    return X,Y

trainX,trainY = ReshapeData(train2,train3)
testX,testY = ReshapeData(test2,test3)

# train
knn.Use_K_Of(15)
knn.Fit(trainX,trainY)

# test

# row = 500
# print(knn.Predict(testX[row,:]))
# print(testY[998])

correctCount = 0
for row in range(0,samplesPerSet*numSets): # 2000
    actualClass = testY[row]
    prediction = knn.Predict(testX[row,:])
    print(row, actualClass, prediction)
    if actualClass == prediction:
        correctCount += 1
print "Percent correct: ", (float(correctCount)/samplesPerSet*numSets) * 100, "%"
print correctCount, "correct"
