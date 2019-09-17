import pickle

class READER:

    def __init__(self):

        pickle_in = open("userData/gesture.p","rb")
        gestureData = pickle.load(pickle_in)
        pickle_in.close()
        print(gestureData)
