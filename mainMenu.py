# main menu concept for testing

import threading
import hashlib
import os
import glob
import shutil
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
    referenceExists = "C:\\Users\\natha\Documents\GitHub\SDNE-Capstone-2023\ReferenceFile\\Reference.txt"
    if os.path.exists(referenceExists):
        os.remove(referenceExists)


#Calculate sha256 hash for various files
def sha256sum():
    file = open("Reference.txt", "w+")
    filenames = glob.glob("C:\\Users\\natha\Documents\GitHub\SDNE-Capstone-2023\Patients\*.txt")
    for f in filenames:
        with open(f, 'rb') as inputfile:
            data = inputfile.read()
            file.writelines(f + "|" + hashlib.sha256(data).hexdigest()+"\n")

    file.close()

    os.rename('C:\\Users\\natha\Documents\GitHub\SDNE-Capstone-2023\\Reference.txt', 'C:\\Users\\natha\Documents\GitHub\SDNE-Capstone-2023\ReferenceFile\\Reference.txt')
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

    with open('reference.txt') as ref:
        pathsAndHashes = ref.readlines()

    for entry in pathsAndHashes:
        hashDict.update({entry.split("|")[0]: entry.split("|")[1]})

        # B-1: Continuously monitor file integrity
    # 25:49, 27:56
    # check inside dictionary if the key exists..
    # if the key doesn't exist, we know that it's a new file
    # if the key does exists and the hash is different, we know that the file has been changed

    print("\nCheck file selected\n")


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