import pickle
import operator

class DataBase:
    file = "userData/database.p"

    def __init__(self):
        try:
            self.database = pickle.load(open(DataBase.file,'rb'))
        except EOFError as err:
            self.reset()
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

        # reset this session's stats:
        self.database[self.currentUser]["currentSession"] = {}

        self.save()

    def incrementDigitAttribute(self,digit,attribute,amount):
        self.database[self.currentUser]["activeDigits"].add(digit)

        if (digit not in self.database[self.currentUser]):
            self.database[self.currentUser][digit] = {}

        if attribute in self.database[self.currentUser][digit]:
            self.database[self.currentUser][digit][attribute] += amount
        else:
            self.database[self.currentUser][digit][attribute] = amount

        # now keep track for this individual session
        if (digit not in self.database[self.currentUser]["currentSession"]):
            self.database[self.currentUser]["currentSession"][digit] = {}

        if attribute in self.database[self.currentUser]["currentSession"][digit]:
            self.database[self.currentUser]["currentSession"][digit][attribute] += amount
        else:
            self.database[self.currentUser]["currentSession"][digit][attribute] = amount


    def digitAttempted(self,digit,correct):
        self.incrementDigitAttribute(digit,"attempted",1)

        if (correct):
            self.incrementDigitAttribute(digit,"correct",1)
            self.incrementDigitAttribute(digit,"incorrect",0)
            self.incrementDigitAttribute(digit,"score",0)

            if (self.getStats(self.currentUser,attribute="score")[digit] < 5):
                self.incrementDigitAttribute(digit,"score",1) # out of past three

        else:
            self.incrementDigitAttribute(digit,"incorrect",1)
            self.incrementDigitAttribute(digit,"correct",0)
            self.incrementDigitAttribute(digit,"score",0)

            if (self.getStats(self.currentUser,attribute="score")[digit] > 0):
                self.incrementDigitAttribute(digit,"score",-1) # out of past three

        self.calcAllSessionPercent(self.currentUser)
        self.save()

    def getStats(self,user,attribute=None):
        digits = {}
        for digit in range(10):
            if digit in self.database[user]:
                if (attribute == None):
                    digits[digit] = self.database[user][digit]
                elif (attribute in self.database[user][digit]):
                    digits[digit] = self.database[user][digit][attribute]

        return digits # returns dictionary of dictionaries with different attributes

    def getThisSessionPercent(self):
        correct = 0
        attempted = 0
        for digit in range(10):
            if digit in self.database[self.currentUser]["currentSession"]:
                correct += self.database[self.currentUser]["currentSession"][digit]["correct"]
                attempted += self.database[self.currentUser]["currentSession"][digit]["attempted"]

        if (attempted > 0):
            percent = float(correct) / float(attempted) * 100
            return percent
        else:
            return 0

    def getAllSessionPercent(self,user):
        # calculate total score if it hasn't been already
        if ("TotalScore" not in self.database[user]):
            self.calcAllSessionPercent(user)

        return self.database[user]["TotalScore"]

    def calcAllSessionPercent(self,user):
        correct = 0
        attempted = 0
        percent = 0
        for digit in range(10):
            if digit in self.database[user]:
                correct += self.database[user][digit]["correct"]
                attempted += self.database[user][digit]["attempted"]
        if (attempted > 0):
            percent = float(correct) / float(attempted) * 100

        self.database[user]["TotalScore"] = percent
        self.save()

    def getTopUsers(self):
        self.calcAllSessionPercent(self.currentUser)
        leaderboard = {}
        for user in self.database:
            score = self.getAllSessionPercent(user)
            leaderboard[user] = score

        top3 = []
        count = 0

        # print(sorted(leaderboard.items(),key=lambda kv: kv[1],reverse=True))
        for item in sorted(leaderboard.items(),key=lambda kv: kv[1],reverse=True):
            if (count < 3):
                top3.append(item)
                count+=1

        return top3

    def getYourRank(self):
        leaderboard = {}
        self.calcAllSessionPercent(self.currentUser)
        for user in self.database:
            score = self.getAllSessionPercent(user)
            leaderboard[user] = score

        count = 0
        for item in sorted(leaderboard.items(),key=lambda kv: kv[1],reverse=True):
            if (item[0] == self.currentUser):
                return count + 1
            count+=1

    def getActiveDigits(self):
        return self.database[self.currentUser]["activeDigits"]

    def reset(self):
        self.database = {}
        self.save()

    def save(self):
        # print("DATABASE:\n\n\n\n"+str(self.database))
        pickle.dump(self.database,open(DataBase.file,'wb'))
