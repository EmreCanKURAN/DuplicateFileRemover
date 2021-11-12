#hashlib for hashing and os for os operations
import hashlib
import os

'''
Removes the given file and returns its size
Input: file(file path)
Output: size(size of the file)
'''
def calcSizeAndDel(file):
    size = os.path.getsize(file)
    os.remove(file)
    return size
'''
Appends same files to the list belongs to specific key(same md5 checksum) in the dictionary.
Input: dupDict(dictionary data structure), dirPath(path of the directory)
'''
def findDups(dupDict, dirPath):
#traverse the folder recursively, that is, including subfolders
    for dirName, subdirList, fileList in os.walk(dirPath):
        for fname in fileList:
        #join dir. name and file name to get the full path
            fullPath = os.path.join(dirName,fname)
        #initialize hash
            hash = hashlib.md5()
        #use "ignore" to avoid errors due to the unicode encoding, and update hash by chunks to avoid memory errors
            with open(fullPath, errors="ignore") as fileToCheck:
            #chunk size can be increased or decreased
                for chunk in iter(lambda: fileToCheck.read(40960), ""):
                    hash.update(str(chunk).encode('utf-8'))
            #unicode->utf-8, use md5 checksum to determine same files
                md5Hash = hash.hexdigest()
            #append if exists
                if md5Hash in dupDict:
                    dupDict[md5Hash].append(fullPath)
            #create and append if does not exist
                else:
                    dupDict[md5Hash] = [fullPath]
'''
Finds duplicate files, removes the ones created later. Keeps the original file. Returns the size of deleted files.
Input: dupDict(dictionary data structure)
Output: totalSize(total size of the deleted files)
'''
def removeDups(dupDict):
    #initialize total size
    totalSize = 0
    #check each md5 hash
    for key in dupDict:
    #if there are more than two files for the same md5 checksum, keep the first created one and remove others
        if(len(dupDict[key]) > 1):
        #print the list of duplicate files to show information
            sameFiles = dupDict[key]
            print(sameFiles)
        #create a list of creation times, since the files are same, it actually does not matter
            ctList = [os.path.getctime(i) for i in sameFiles]
        #get the index of the minimum (first created)
            minIdx = ctList.index(min(ctList))
        #remove others and keep the original, sum the size of the deleted files (calcSizeAndDel func.)
            totalSize = totalSize + sum([calcSizeAndDel(i) for i in sameFiles if sameFiles.index(i) != minIdx])
    return totalSize

'''
Main function
'''
def main():
#the folder needs to get checked
    dirPath='C:\\Users\\hypc7\\Desktop'
#initializing dictionary data structure to keep duplicates as key-value pairs
    dupDict = dict()
#calling functions
    findDups(dupDict, dirPath)
    totalSize = removeDups(dupDict)
#convert "bytes" to "megabytes" and limit to two decimal points
    print("Recovered:%.2f MBs" % (totalSize/(1024**2)))

#run main
if __name__ == "__main__":
    main()
