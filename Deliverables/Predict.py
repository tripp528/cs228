import matplotlib.pyplot as plt
import numpy as np

from knn import KNN

# load dataset
knn = KNN()
knn.Load_Dataset('iris.csv')
x = knn.data[:,0]
y = knn.data[:,1]
# slice dataset
trainX = knn.data[::2,1:3]
trainY = knn.target[::2]
testX = knn.data[1::2,1:3]
testY = knn.target[1::2]

# train
knn.Use_K_Of(15)
knn.Fit(trainX,trainY)

# test
wrongCount = 0
for i in range(len(testY)):
    actualClass = testY[i]
    prediction = knn.Predict(testX[i,:])
    print(actualClass, prediction)
    if actualClass != prediction:
        wrongCount += 1
print "Percent correct: ", (1 - float(wrongCount)/len(testY)) * 100, "%"


# PLOT:
colors = np.zeros((3,3),dtype='f')
colors[0,:] = [1,0.5,0.5]
colors[1,:] = [0.5,1,0.5]
colors[2,:] = [0.5,0.5,1]

plt.figure()
# plt.scatter(trainX[:,0],trainX[:,1],c=trainY)
# plt.scatter(testX[:,0],testX[:,1],c=trainY)

[numItems,numFeatures] = knn.data.shape
for i in range(0,numItems/2):
    itemClass = int(trainY[i])
    currColor = colors[itemClass,:]
    plt.scatter(trainX[i,0],trainX[i,1],c=currColor,s=50,lw=2,edgecolor='black')

for i in range(0,numItems/2):
    itemClass = int(testY[i])
    currColor = colors[itemClass,:]
    prediction = int(knn.Predict(testX[i,:]))
    edgeColor = colors[prediction,:]
    plt.scatter(testX[i,0],testX[i,1],c=currColor,s=50,lw=2,edgecolor=edgeColor)

plt.show()
