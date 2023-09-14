# main menu concept for testing

import threading
import hashlib
import os
import glob
import time
import http.server
import socketserver




# display main menu
def mainMenu():
    print("---Main menu---")
    print("[1] Create new reference text file")#TODO:update wording regarding creation/updating of reference files.
    print("[2] Check files to reference hash")
    print("[3] Compare File to previous Versions")
    print("[0] Exit program")


hashDict = {}
dateDict = {}


# Deletes previously existing reference file
def deleteReference():
    print("Updating Previous reference file")
    referencePath = "ReferenceFile\Reference.txt"
    dateReferencePath = "ReferenceFile\DateReference.txt"
    if os.path.exists(referencePath):
        os.remove(referencePath)

    if os.path.exists(dateReferencePath):
        os.remove(dateReferencePath)


# Calculate sha256 hash for various files
def sha256sum():
    file = open("Reference.txt", "w+")
    fileNames = glob.glob("Patients\*.txt")
    for f in fileNames:
        with open(f, 'rb') as inputFile:
            data = inputFile.read()
            file.writelines(f + "|" + hashlib.sha256(data).hexdigest() + "\n")

    file.close()

    os.replace("Reference.txt", "ReferenceFile\Reference.txt")

def dateFileSum():
    # Create a new file instead of the hash include the last date of file modification for each patient

    datefile = open("DateReference.txt", "w+")
    dateFileNames = glob.glob("Patients\*.txt")

    for d in dateFileNames:
        with open(d, 'rb') as inputFile:
            data = inputFile.read()
            datefile.writelines(d + "|" + str(time.ctime(os.path.getmtime(d))) + "\n")

    datefile.close()
    os.replace("DateReference.txt", "ReferenceFile\DateReference.txt")


# return statement in this def only returns the first file and does not cycle to file b and onwards.


# Create reference

def createReferenceFile():
    # Calculate hashes for each patient file and store in reference.txt file
    # Calculate Hash from the patient files and store in reference.txt
    # Collect all files in the patients folder
    # path = "C:\\Users\\natha\Documents\GitHub\SDNE-Capstone-2023\Patients"
    # files = os.listdir(path)
    deleteReference()
    sha256sum()
    dateFileSum()
    # file = open("testReference.txt", "w+")
    # f.writelines(sha256sum())
    # f.close()

    # for f in files:
    #     absfilepath = os.path.abspath(f)
    #     sha256sum(f)
    #
    #     print(absfilepath + '|' + f)


# Check files
def checkFile():
    # B-0: Load file/hash pairs from reference.text and store then in a dictionary
    # key = file path
    # value = corresponding file hash
    # line=1
    referencePath = "ReferenceFile\Reference.txt"

    if not os.path.exists(referencePath):
        # One of the Reference.txt has been deleted
        print(referencePath + "Has been removed!")
        return

    with open('ReferenceFile\Reference.txt') as ref:
        pathsAndHashes = ref.readlines()

    for entry in pathsAndHashes:
        # line+=1
        # if line % 2 == 0:
        hashDict.update({entry.split("|")[0]: entry.split("|")[1].strip()})
    # print(hashDict.keys())
    # print(hashDict.values())

    # B-1: Continuously monitor file integrity
    # 25:49, 27:56
    # check inside dictionary if the key exists..
    # if the key doesn't exist, we know that it's a new file
    # if the key does exists and the hash is different, we know that the file has been changed
    # for keys,values in hashDict.items():

    while True:
        print("Beginning Check...")
        time.sleep(5)

        # Calculating each file Hash in patients folder to compre directly to hashDict key/value pairs.
        fileNamesToCompare = glob.glob("Patients\*.txt")
        for f in fileNamesToCompare:
            comparingHash = hashlib.sha256(open(f, 'rb').read()).hexdigest()

            if not hashDict.__contains__(f):
                # a new file has been created that is not in the reference file!
                print(f + " has been created!")
            else:
                if hashDict[f] == comparingHash:
                    print()
                else:
                    # file has been compromised, notify the user!
                    print(f + " has changed!")

            # Line 98-99 is an issue, something to do with Key,value comparing with the comparing hash and f. Must look into it to complete B
            # Error was caused due to Dictionary having '\n' attached to the value, using strip() on line 75 resolves issue

        # check if a file has been deleted
        for key in hashDict.keys():
            if key not in fileNamesToCompare:
                # file in reference.txt has been deleted, notify the user!
                print(key + " has been deleted!")
                return

        # I have kept Line 125-131 but commented them they've been tested
        # It does nothing yet. it is advised to be removed.
        # for k in hashDict.keys():
        #    referenceExists = "ReferenceFile\Reference.txt"

        #    if not os.path.exists(referenceExists):
        #        #One of the Reference.txt has been deleted
        #        print(k + " Has Been Deleted!")

        print("Concluded Check...\n\n")
        return
        # def printIt():
        #    threading.Timer(1.0, printit).start()
        #    print("Checking if files match...")

        # printIt()

        # this is from the new file
        # files =  # get a.txt, b.txt etc.
        #
        # # for each file, calculate the hash and add it to the reference.txt
        # for file in files:
        #
        #     if hashDict[file.path] == null:
        #         # a new file has been created!
        #         print(hash.path + "has been created!")
        #     else:
        #         if hashDict[file.path] == file.hash:
        #         # notify if a file has been changed
        #         else:
        #             # file has been compromised, notify the user!
        #             print(hash.path + "has changed!")
        #
        #     for key in hashDict.keys:
        #         # file in reference.txt has been deleted, notify the user!
        #         if
        #             print(hash.path + "has been deleted!")


# Check for specific file name, contents and datestamp of the file.
# Will have to do various things for version control
# -Ensure the file has the same name as the one in the repo (done)
# -Ensure the file has the same date, if not, announce a new version has been created
def checkSpecificFile():

    print("Please enter which filename you wish to compare previous versions to. Do not include file extension\nFiles Available:")
    fileNames = glob.glob("Patients\*.txt")

    with open('ReferenceFile\DateReference.txt') as ref:
        pathsAndDates = ref.readlines()

    for entry in pathsAndDates:
        dateDict.update({entry.split("|")[0]: entry.split("|")[1].strip()})
    # print(dateDict.keys())
    # print(dateDict.values())

    for f in fileNames:
        print(f + "\n")

    fileSelection = "Patients\\" + (input("Select the Patient Name")) + ".txt"

    for f in fileNames:

        comparingDate = (time.ctime(os.path.getmtime(f)))

        if f == fileSelection:
            print(f + " selected")
            # Code Check for date
            if dateDict[f].__contains__(comparingDate):
                print("MATCH IN DATE")
                return
            else:
                print("File " + f + " is a new version, last modified on " + comparingDate)
                return
        # if not fileSelection.__contains__(f):
        #     print("file does not exist")
        #     break
    print("file does not exist")
    checkSpecificFile()






#     # START OF EXECUTION
#
# # Launch http Server to monitor files on another computer
# PORT = 8000
#
# Handler = http.server.SimpleHTTPRequestHandler
#
# with socketserver.TCPServer(("192.168.2.180", PORT), Handler) as httpd:
#     print("serving at port", PORT)
#     httpd.serve_forever()


mainMenu()


userSelection = int(input("\nWhat would you like to do? "))



while userSelection != 0:
    if userSelection == 1:
        # create new reference here
        createReferenceFile()

    elif userSelection == 2:
        # create new reference here
        checkFile()

    elif userSelection == 3:
        # Investigate Version
        checkSpecificFile()

    else:
        # create new reference here
        print("\nInvalid option selected\n")

    mainMenu()
    userSelection = int(input("\nWhat would you like to do? "))

print("\nTerminating session...goodbye!")
