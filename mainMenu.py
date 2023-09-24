# main menu concept for testing
import codecs
import threading
import hashlib
import os
import glob
import time
import http.server
import socketserver
import asyncio
from cryptography.fernet import Fernet
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
from multiprocessing import Pool


# Checker Boolean values for OPTION 2:
E0 = False  # Check if Reference file got deleted before-hand
E1 = False  # Check for if new patient file got added and does not line up with reference file
E2 = False  # Check if Hash does not match file, file has been compromised
E3 = False  # Check if Reference file was deleted after main checks were completed
E4 = False  # Check if Date file does not match anything in date_reference file
E5 = False  # Check if file does not exist, last check.


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ssk'  # protects csrf attacks
app.config['UPLOAD_FOLDER'] = 'NewPatients'


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")


@app.route('/', methods=['GET', "POST"])
@app.route('/home', methods=['GET', "POST"])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                               secure_filename(file.filename)))  # may need to change abspath to relative path
        return "File has been uploaded."
    return render_template("index.html", form=form)


@app.route('/alert/', methods=['GET', "POST"])
async def alert():

    await checkFile() #OPTION 2 WILL NOT WORK AS LONG AS checkfile() WILL USE Asynchornous method call to fix.
    if E1 == True:
        message = "Alert E1 triggered"
        return render_template('alert.html', message=message)
    if E2 == True:
        message = "Alert E2 triggered"
        return render_template('alert.html', message=message)
    if E3 == True:
        message = "Alert E3 triggered"
        return render_template('alert.html', message=message)
    if E4 == True:
        message = "Alert E4 triggered"
        return render_template('alert.html', message=message)
    if E5 == True:
        message = "Alert E5 triggered"
        return render_template('alert.html', message=message)
    return render_template('alert.html')


if __name__ == '__main__':
    app.run(debug=True)


# display main menu
def mainMenu():
    print("---Main menu---")
    print("[1] Create new reference text file")  # TODO:update wording regarding creation/updating of reference files.
    print("[2] Check files to reference hash")
    print("[3] Compare File to previous Versions")
    print("[0] Exit program")


hashDict = {}
dateDict = {}


key = Fernet.generate_key()
with open('mykey.key', 'wb') as mykey:
    mykey.write(key)
fk = Fernet(key)


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

    with open('ReferenceFile\Reference.txt', 'rb') as originalFile:
        original = originalFile.read()
    encrypted = fk.encrypt(original)

    with open('enc_Reference.txt', 'wb') as encryptedFile:
        encryptedFile.write(encrypted)

    os.replace("enc_Reference.txt", "ReferenceFile\enc_Reference.txt")


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

    with open('ReferenceFile\DateReference.txt', 'rb') as originalFile:
        original = originalFile.read()
    encrypted = fk.encrypt(original)

    with open('enc_DateReference.txt', 'wb') as encryptedFile:
        encryptedFile.write(encrypted)

    os.replace("enc_DateReference.txt", "ReferenceFile\enc_DateReference.txt")


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
async def checkFile():
    # ADD A SECTION THAT CREATES A NEW ENCRYPTED VERSION OF THE CURRENT REFERENCE FILES.

    # B-0: Load file/hash pairs from reference.text and store then in a dictionary
    # key = file path
    # value = corresponding file hash
    # line=1
    referencePath = "ReferenceFile\enc_Reference.txt"

    if not os.path.exists(referencePath):
        # One of the Reference.txt has been deleted
        print(referencePath + "Has been removed!")
        E0 = True
        return

    with open('ReferenceFile\enc_Reference.txt', 'rb') as enc_ref:
        encrypted = enc_ref.read()
    decrypted = fk.decrypt(encrypted)

    with open('dec_Reference.txt', 'wb') as dec_ref:
        dec_ref.write(decrypted)

    with open('dec_Reference.txt', 'r') as dec:
        pathsAndHashes = dec.readlines()
        print(pathsAndHashes)
    for entry in pathsAndHashes:
        # line+=1
        # if line % 2 == 0:
        hashDict.update({entry.split("|")[0]: entry.split("|")[1].strip()})

    os.replace("dec_Reference.txt", "ReferenceFile\dec_Reference.txt")
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
                E1 = True
            else:
                if hashDict[f] == comparingHash:
                    print()
                else:
                    # file has been compromised, notify the user!
                    print(f + " has changed!")
                    E2 = True

            # Line 98-99 is an issue, something to do with Key,value comparing with the comparing hash and f. Must look into it to complete B
            # Error was caused due to Dictionary having '\n' attached to the value, using strip() on line 75 resolves issue

        # check if a file has been deleted
        for key in hashDict.keys():
            if key not in fileNamesToCompare:
                # file in reference.txt has been deleted, notify the user!
                print(key + " has been deleted!")
                E3 = True
                return

        # I have kept Line 125-131 but commented them they've been tested
        # It does nothing yet. it is advised to be removed.
        # for k in hashDict.keys():
        #    referenceExists = "ReferenceFile\Reference.txt"

        #    if not os.path.exists(referenceExists):
        #        #One of the Reference.txt has been deleted
        #        print(k + " Has Been Deleted!")

        print("Concluded Check...\n\n")
        print("Deleted Decrypted Files")
        os.remove("ReferenceFile\dec_Reference.txt")

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
    print(
        "Please enter which filename you wish to compare previous versions to. Do not include file extension\nFiles Available:")
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
                E4 = True
                return
        # if not fileSelection.__contains__(f):
        #     print("file does not exist")
        #     break
    print("file does not exist")
    E5 = True
    checkSpecificFile()


# #     #START OF EXECUTION
# #
# IP FOR SHERIDAN: 10.16.44.141
# IP FOR HOME: 192.168.2.180
# #Launch http Server to monitor files on another computer
# PORT = 8000
#
# Handler = http.server.SimpleHTTPRequestHandler
#
# with socketserver.TCPServer(("10.16.44.141", PORT), Handler) as httpd:
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

asyncio.run(alert())