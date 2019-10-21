import pickle
database = pickle.load(open('userData/database.p','rb'))

userName = raw_input('Please enter your name: ')
if userName in database: # not new user
    database[userName]['logins'] += 1

    print("welcome back " + userName + '.')

else: # new user
    database[userName] = {}
    database[userName]['logins'] = 1
    print("welcome " + userName + '.')

print(database)
pickle.dump(database,open('userData/database.p','wb'))
