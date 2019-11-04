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

            self.database[self.currentUser]["activeDigits"] = {1,}
            


        self.save()

    def incrementDigitAttribute(self,digit,attribute,amount):
        self.database[self.currentUser]["activeDigits"].add(digit)

        if (digit not in self.database[self.currentUser]):
            self.database[self.currentUser][digit] = {}

        if attribute in self.database[self.currentUser][digit]:
            self.database[self.currentUser][digit][attribute] += amount
        else:
            self.database[self.currentUser][digit][attribute] = amount


    def digitAttempted(self,digit,correct):
        self.incrementDigitAttribute(digit,"attempted",1)

        if (correct):
            self.incrementDigitAttribute(digit,"correct",1)
            self.incrementDigitAttribute(digit,"incorrect",0)
            self.incrementDigitAttribute(digit,"score",0)

            if (self.getStats(attribute="score")[digit] < 5):
                self.incrementDigitAttribute(digit,"score",1) # out of past three

        else:
            self.incrementDigitAttribute(digit,"incorrect",1)
            self.incrementDigitAttribute(digit,"correct",0)
            self.incrementDigitAttribute(digit,"score",0)

            if (self.getStats(attribute="score")[digit] > 0):
                self.incrementDigitAttribute(digit,"score",-1) # out of past three

        self.save()

    def getStats(self,attribute=None):
        digits = {}
        for digit in range(10):
            if digit in self.database[self.currentUser]:
                if (attribute == None):
                    digits[digit] = self.database[self.currentUser][digit]
                elif (attribute in self.database[self.currentUser][digit]):
                    digits[digit] = self.database[self.currentUser][digit][attribute]

        return digits # returns dictionary of dictionaries with different attributes

    def getActiveDigits(self):
        return self.database[self.currentUser]["activeDigits"]

    def reset(self):
        self.database = {}
        self.save()

    def save(self):
        print(self.database)
        pickle.dump(self.database,open(DataBase.file,'wb'))
