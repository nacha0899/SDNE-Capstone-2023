# main menu concept for testing


# display main menu
def mainMenu():
    print("---Main menu---")
    print("[1] Create new reference text file")
    print("[2] Check files to reference hash")
    print("[0] Exit program")


hashDict = {}


# Create reference
def createReferenceFile():
    print("\nCreate reference selected\n")


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