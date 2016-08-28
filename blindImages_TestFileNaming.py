#! /usr/bin/env python3
#blindFiles.py--- the functions blindImages and unblind take a file path as an argument. blindImages counts the tif
#files and determines how many random numbers you need to blind the files.
#then it renames and copies the files to a new directory.
#unblind reverses this option. For safety, blindFiles and unBlind copy the files before renaming them so the originals are unaffected. 
'''by Nick George on August 3, 2016'''

import random, shutil, os, pprint, shelve

def blindImages(filePath): #HARDCODED_VARIABLE... make this an option in a GUI
    try:
        i=0
        fileCount=0
        for filename in os.listdir(filePath):
            if filename.endswith('.tif'): #HARDCODED_VARIABLE... make an option in a GUI for a number of file types
                fileCount+=1
            else:
                continue
        randomList=random.sample(range(100,999),fileCount)
        blindKey={}
        i=0
        newFile='keyFileFor_'+str(os.path.basename(filePath))
        baseName=str(os.path.basename(filePath))
        keyShelf=shelve.open(newFile) #open shelf file to store the stuff for later retrieval.
        os.makedirs(os.path.join(filePath,'BlindImages_for_%s'%(baseName))) #Handle exception and throw error if this file exists.
        keyFile=open(str(newFile)+'.txt','w')
        shutil.move(str(newFile)+'.txt',os.path.join(filePath,'BlindImages_for_%s' %(baseName)))#move the new files to the new BlindFolder Directory. 
        shutil.move(str(newFile+'.db'), os.path.join(filePath,'BlindImages_for_%s' %(baseName))) #move the new binary file to the new BlindFolder Directory. 
        for filename in os.listdir(filePath):
            if filename.endswith('.tif'): #HARDCODED_VARIABLE
                blindKey[filename]=randomList[i]
                #copy the tif files into the new folder within the directory. 
                shutil.copy(os.path.join(filePath,filename),os.path.join(filePath,'BlindImages_for_%s' %(baseName),str(randomList[i])+'.tif')) #HARDCODED_VARIABLE
                i+=1
        pprint.pprint(blindKey) # to the terminal, print the key. 
        keyFile.write(pprint.pformat(blindKey)) # save in a nice format to a key file. 
        keyShelf['Key']=blindKey # save it to the binary file under the key 'Key' #HARDCODED_VARIABLE
        keyFile.close()
        keyShelf.close()
        print('Done')
    except FileExistsError:
        print('Uh Oh... Looks like you already blinded the files in this directory or a \n BlindImages_for_%s folder already exists'%(baseName))

def unBlind(filePath):
    try:
        baseName=str(os.path.basename(filePath))
        newFile='keyFileFor_'+str(os.path.basename(filePath))
        os.makedirs(os.path.join(filePath,'UnblindedImages_for_%s'%(baseName))) 
        BlindDir= os.listdir(os.path.join(filePath,'BlindImages_for_%s' %(baseName))) 
        os.chdir(os.path.join(filePath,'BlindImages_for_%s'%(baseName)))
        #code decrptying using the .db shelf file.
        keyShelf=shelve.open(newFile)
        blindKey=keyShelf['Key']
        for k,v in blindKey.items():
            for filename in BlindDir:
                if str(v) in filename:
                    shutil.copy(os.path.join(filePath,'BlindImages_for_%s' %(baseName),filename),os.path.join(filePath,'UnblindedImages_for_%s'%(baseName),k)) 
                else:
                    continue
        print('Done.')
    except FileExistsError:
        print('Uh Oh... Looks like you already unblinded the files in this directory or a \n UnblindedImages_for_%s folder already exists.'%(baseName))
def runProgram():
    while True:
        print('Would you like to blind or unblind files? (please type blind or unblind or nothing to quit)')
        mode=input()
        if mode.lower()=='blind':
            print('Please enter the path for the folder you would like to work with')
            filePath=input()
            if os.path.isdir(filePath):
                blindImages(filePath)
                break
            else:
                print('enter a valid filename')
                continue
        elif mode.lower()=='unblind':
            print('please enter the filepath for the original files.')
            filePath=input()
            if os.path.isdir(filePath):
                unBlind(filePath)
                break
            else:
                print('enter a valid filename')
                continue
        elif mode.lower()=='':
            break
        else:
            print('you should follow instructions')
            continue
            
            
        
runProgram()
#TODO: Make a GUI https://www.youtube.com/watch?v=Qr60hWFyKHc 
# with the GUI, give choices for all locations with a HARDCODED_VARIABLE label. 
