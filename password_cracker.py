#!usr/bin/python3

import hashlib

#get all passwords and salts from database
file=open("top-10000-passwords.txt", "r")
passwords=file.read().split("\n")

file=open("known-salts.txt", "r")
salts=file.read().split("\n")

#dictionary to store passwords and their hash (this is not recommended in general)
passwordHash = {}
#dictionary to store all passwords and their hash with known-salts
passwordSaltHash = {}

#function to generate dictionaries
def generateWithoutSalts():
    for password in passwords:
        hash_sha1 = hashlib.sha1(password.encode()).hexdigest()
        passwordHash[hash_sha1] = password

# print(passwordHash)

def generateWithSalts():
    for salt in salts:
        for password in passwords:
            #prepending salt to password
            prepended = salt+password
            hash_sha1 = hashlib.sha1(prepended.encode()).hexdigest()
            passwordSaltHash[hash_sha1] = password
            #appending salt to password
            appended = password+salt
            hash_sha1 = hashlib.sha1(appended.encode()).hexdigest()
            passwordSaltHash[hash_sha1] = password

#calling above functions
generateWithoutSalts()
generateWithSalts()

#function to crack password
def crack_sha1_hash(hash, use_salts=False):
    #if use_salts is true
    if use_salts==True:
        return passwordSaltHash.get(hash, "PASSWORD NOT IN DATABASE")
    
    #if use_salts is false
    return passwordHash.get(hash, "PASSWORD NOT IN DATABASE")

print(crack_sha1_hash("53d8b3dc9d39f0184144674e310185e41a87ffd5", True))

#---------------------------------------------------------------------------------------#
#to be used for self testing

# print("53d8b3dc9d39f0184144674e310185e41a87ffd5")
# print("-----------------------------------------")

# for salt in salts:
#     print(hashlib.sha1(("superman"+salt).encode()).hexdigest())
#     print(hashlib.sha1((salt+"superman").encode()).hexdigest())