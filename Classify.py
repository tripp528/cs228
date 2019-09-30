import pickle
import numpy as np



pickle_in = open("userData/train2.p","rb")
gestureData = pickle.load(pickle_in)
pickle_in.close()
print(gestureData.shape)
