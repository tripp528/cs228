import pickle

class DataBase:
    file = "../userData/database.p"

    def __init__(self):
        self.database = pickle.load(open(DataBase.file,'rb'))

    def login(self):
        userName = raw_input('Please enter your name: ')
        self.currentUser = userName
        if userName in self.database: # not new user
            self.database[userName]['logins'] = self.database[userName]['logins'] + 1
            print("welcome back " + userName + '.')

        else: # new user
            self.database[userName] = {}
            self.database[userName]['logins'] = 1
            print("welcome " + userName + '.')

        self.save()

    def addData(self,key,value):
        self.database[self.currentUser][key] = value
        self.save()

    def incrementDigitCount(self,digit):
        key = "digit"+str(digit)+"attempted"

        if key in self.database[self.currentUser]:
            value = self.database[self.currentUser][key] + 1
        else:
            value = 1

        self.addData(key,value)

    def getDigitCounts(self):
        digits = {}
        for digit in range(10):
            key = "digit"+str(digit)+"attempted"
            if key in self.database[self.currentUser]:
                digits[digit] = self.database[self.currentUser][key]
                
        return digits

    def reset(self):
        self.database = {}
        self.save()

    def save(self):
        print(self.database)
        pickle.dump(self.database,open(DataBase.file,'wb'))
