# main menu concept for testing

import threading
import hashlib
import os
import glob
import time
# display main menu
def mainMenu():
    print("---Main menu---")
    print("[1] Create new reference text file")
    print("[2] Check files to reference hash")
    print("[0] Exit program")


hashDict = {}

#Deletes previously existing reference file
def deleteReference():
    print("Deleting Previous reference file")
    referenceExists = "ReferenceFile\Reference.txt"
    if os.path.exists(referenceExists):
        os.remove(referenceExists)


#Calculate sha256 hash for various files
def sha256sum():
    file = open("Reference.txt", "w+")
    filenames = glob.glob("Patients\*.txt")
    for f in filenames:
        with open(f, 'rb') as inputfile:
            data = inputfile.read()
            file.writelines(f + "|" + hashlib.sha256(data).hexdigest()+"\n")

    file.close()

    os.replace("Reference.txt", "ReferenceFile\Reference.txt")
# return statement in this def only returns the first file and does not cycle to file b and onwards.


# Create reference

def createReferenceFile():
    #Calculate hashes for each patient file and store in reference.txt file
    # Calculate Hash from the patient files and store in reference.txt
    # Collect all files in the patients folder
    # path = "C:\\Users\\natha\Documents\GitHub\SDNE-Capstone-2023\Patients"
    # files = os.listdir(path)
    deleteReference()
    sha256sum()
    #file = open("testReference.txt", "w+")
    #f.writelines(sha256sum())
    #f.close()


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

    with open('C:\\Users\\natha\Documents\GitHub\SDNE-Capstone-2023\ReferenceFile\\Reference.txt') as ref:
        pathsAndHashes = ref.readlines()

    for entry in pathsAndHashes:
        hashDict.update({entry.split("|")[0]: entry.split("|")[1]})

        # B-1: Continuously monitor file integrity
    # 25:49, 27:56
    # check inside dictionary if the key exists..
    # if the key doesn't exist, we know that it's a new file
    # if the key does exists and the hash is different, we know that the file has been changed
    # for keys,values in hashDict.items():
    #     print(keys)
    #     print(values)

    while True:
        print("Beginning Check...")
        time.sleep(3)

        #Calculating each file Hash in patients folder to compre directly to hashDict key/value pairs.
        filenamescompare = glob.glob("C:\\Users\\natha\Documents\GitHub\SDNE-Capstone-2023\Patients\*.txt")
        for f in filenamescompare:
            comparinghash = hashlib.sha256(open(f, 'rb').read()).hexdigest()
            print(comparinghash)

            if hashDict[f] == 0:
                # a new file has been created!
                print(f + "has been created!")
            else:
                if hashDict[f] == comparinghash:
                    print()
                else:
                    # file has been compromised, notify the user!
                    print(f + "has changed!")

            # Line 98 is an issue, something to do with Key,value comparing with the comparing hash and f. Must look into it to complete B

        for k in hashDict.keys():
            referenceExists = "C:\\Users\\natha\Documents\GitHub\SDNE-Capstone-2023\ReferenceFile\\Reference.txt"

            if not os.path.exists(referenceExists):
                #One of the Reference.txt has been deleted
                print(k + "Has Been Deleted!")

        print("Concluded Check...")
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


            # START OF EXECUTION
mainMenu()
userSelection = int(input("\nWhat would you like to do? "))

while userSelection != 0:
    if userSelection == 1:
        # create new reference here
        createReferenceFile()

    elif userSelection == 2:
        # create new reference here
        checkFile()

    else:
        # create new reference here
        print("\nInvalid option selected\n")

    mainMenu()
    userSelection = int(input("\nWhat would you like to do? "))

print("\nTerminating session...goodbye!")