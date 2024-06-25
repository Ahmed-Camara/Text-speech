import pyttsx3
import os.path
import os
import common as c
import base64
import shutil
import win32security
import ntsecuritycon as con
import datetime
import uuid
import gzip
import io


def set_directory_permissions(path):
    try:
        user, domain, type = win32security.LookupAccountName("", os.getlogin())
        sd = win32security.GetFileSecurity(path, win32security.DACL_SECURITY_INFORMATION)
        dacl = sd.GetSecurityDescriptorDacl()
        dacl.AddAccessAllowedAce(win32security.ACL_REVISION, con.FILE_GENERIC_WRITE | con.FILE_GENERIC_READ | con.FILE_GENERIC_EXECUTE, user)
        sd.SetSecurityDescriptorDacl(1, dacl, 0)
        win32security.SetFileSecurity(path, win32security.DACL_SECURITY_INFORMATION, sd)
    except Exception as e:
        print(f"Echec de l'attribution des permissions: {e}")


"""
def FlushRepository():

    #f = "/src/AUDIO"
    #f = "C:/xampp/htdocs/AUDIO"
    f = c.PATH_FOLDER.rsplit('/', 1)[0]
    print("f : ",f)
    with os.scandir(f) as entries:
        for entry in entries:
            if entry.is_dir() and not entry.is_symlink():
                shutil.rmtree(entry.path)
            else:
                os.remove(entry.path)
"""
def writeToFile(files,textFiles):
    with open(files, "rb") as f1,open(textFiles, "w") as f2:
        encoded_f1 = base64.b64encode(f1.read())
        f2.write("data:audio/mp4;base64,")
        f2.write(str(encoded_f1))
    

def compress_base64_data(data):
    out = io.BytesIO()
    with gzip.GzipFile(fileobj=out, mode='w') as f:
        f.write(data.encode('utf-8'))
    compressed_data = out.getvalue()
    return base64.b64encode(compressed_data).decode('utf-8')

    
def readFromFile(files):
    text_file = open(files, "r")
    data = text_file.read()
    text_file.close()
    return data

def generate_unique_string():
    unique_id = uuid.uuid4()
    return str(unique_id)

def getBase64Files(filePath,path):
    TxtFiles = path+"/base64_"+generate_unique_string()+".txt"
    writeToFile(filePath,TxtFiles)
    data = readFromFile(TxtFiles)
    return data

def FlushRepository(f):
    with os.scandir(f) as entries:
        for entry in entries:
            if entry.is_dir() and not entry.is_symlink():
                shutil.rmtree(entry.path)
            else:
                os.remove(entry.path)

def handleRepository(repository):
    set_directory_permissions(repository.rsplit('/', 1)[0])
    
    if not os.path.exists(repository.rsplit('/', 1)[0]):
        os.makedirs(repository.rsplit('/', 1)[0])
        
    if not os.path.exists(repository):
        FlushRepository(repository.rsplit('/', 1)[0])
        os.makedirs(repository)
 

from gtts import gTTS
def generateAudio(text, lang, ticket, paths):
    #if not os.path.exists(c.PATH_FOLDER):
        #set_directory_permissions(c.PATH_FOLDER)
        #FlushRepository(c.PATH_FOLDER.rsplit('/', 1)[0])
        #os.makedirs(c.PATH_FOLDER)
    handleRepository(c.PATH_FOLDER)
    audioName = "/audio_"+lang+"_"+ticket+".mp4"
    AudioFiles = c.PATH_FOLDER + audioName
    TxtFiles = c.PATH_FOLDER+"/base64_"+lang+"_"+ticket+".txt"
    
    engine = pyttsx3.init()
    engine.save_to_file(text, AudioFiles)
    engine.runAndWait()
    
    lists = paths.split("/")
    audio = lists[0]
    subFold = lists[1]
    
    audioURL = c.http+c.address+"/"+audio+"/"+subFold+audioName
    
    writeToFile(AudioFiles,TxtFiles)
    data = readFromFile(TxtFiles)
    textSpeech = gTTS(text=text, lang=lang)
    return audioURL,data 
 

"""
def generateAudio(text,lang,ticket,paths):
   
    if not os.path.exists(c.PATH_FOLDER):
        FlushRepository()
        os.makedirs(c.PATH_FOLDER)

    audioName = "/audio_"+lang+"_"+ticket+".mp4"
    
    AudioFiles = c.PATH_FOLDER + audioName

    TxtFiles = c.PATH_FOLDER+"/base64_"+lang+"_"+ticket+".txt"
    textSpeech = gTTS(text=text, lang=lang)
    textSpeech.save(AudioFiles)
    lists = paths.split("/")
    audio = lists[0]
    subFold = lists[1]

    audioURL = c.http+c.address+"/"+audio+"/"+subFold+audioName

    writeToFile(AudioFiles,TxtFiles)
    data = readFromFile(TxtFiles)

    return audioURL,data
"""

