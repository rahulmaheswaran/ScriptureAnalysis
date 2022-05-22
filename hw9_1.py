import re
from string import digits
#Arguments:
#  filename: name of file to read in
#Returns: a list of strings
# each string is one line in the file, 
# and all of the characters should be lowercase, have no newlines, and have both a prefix and suffix of '__' (2 underscores)
#Notes: make sure to pad the beginning and end of the string with '_'
#       make sure the string does not contain newlines
#       make sure to convert the string to lower-case
#       so "Hello World" should be turned into "__hello world__"
#hints: https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files
#       https://docs.python.org/3/library/stdtypes.html#str.splitlines

def getFormattedText(filename):
    #fill in
    pref = '__'
    with open(filename, "r") as f:
        text = f.read()
        text = re.sub(r"^\d+\s|\s\d+\s|\s\d+$", "", text)
       # text = re.sub(r'\d+', "", text)
        lines = text.splitlines()
        lines = [pref + x.strip().lower() + pref for x in lines]


    return lines
        
        

#Arguments:
#  line: a string of text
#Returns: a list of 3-character n-gram
def getNgrams(line):
    #fill in
    n = 3
    nGrams = []
    '''
    for i in range(len(line)-n+1):
        if not line[i:i+n].isdigit():
            nGrams.append(line[i:i+n]) 
    '''
    nGrams = [line[i:i+n] for i in range(len(line)-n+1)]


    '''
        for i in range(len(nGrams)):
        count = 0
        for j in range(n):
            if nGrams[i][j].isnumeric():
                count = 1
        if count == 1:
            tmp.append(nGrams[i])
    
    '''


    return nGrams


#Arguments:
#  filename: the filename to create an n-gram dictionary for
#Returns: a dictionary
#  where ngrams are the keys and the count of that ngram is the value.
#Notes: Remember that getFormattedText gives you a list of lines, and you want the ngrams from
#       all the lines put together.
#       You should use getFormattedText() and getNgrams() in this function.
#Hint: dict.fromkeys(l, 0) will initialize a dictionary with the keys in list l and an
#      initial value of 0

def getDict(filename):
    #fill in
    nGramDict = {}
    n = 3
    #Get lines
    lines = getFormattedText(filename)
    for string in lines:
        nGramDict.update(dict.fromkeys(getNgrams(string),0)) #Initialize a key for each 3gram

    for str in lines:
        for i in range(len(str)-n+1):
            nGramDict[str[i:i+n]] += 1


    return nGramDict

#Arguments:
#   filename: the filename to generate a list of top N (most frequent n-gram, count) tuples for
#   N: the number of most frequent n-gram tuples to have in the output list.
#Returns: a list of N tuples 
#   which represent the (n-gram, count) pairs that are most common in the file.
#   To clarify, the first tuple in the list represents the most common n-gram, the second tuple the second most common, etc...
#You may find the following StackOverflow post helpful for sorting a dictionary by its values: 
#Also consider the dict method popitem()
#https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
def topNCommon(filename,N):
    dict = getDict(filename)
    commonN = []

    temp = ({k: v for k, v in sorted(dict.items(), key=lambda item: item[1])})
    for i in range(N):
        commonN.append(temp.popitem())

    return commonN

########################################## Checkpoint, can test code above before proceeding #############################################

#Arguments:
#   fileNamesList: a list of filepath strings for the different language text files to process
#Returns: a list of dictionaries 
#   where each dictionary corresponds to one of the filepath strings.
#   Each dictionary in the list
#   should have keys corresponding to the n-grams, and values corresponding to the count of the n-gram
#Hint: Use functions defined in previous step.
def getAllDicts(fileNamesList):
    langDicts = []
    for filename in fileNamesList:
        langDicts.append(getDict(filename))
    

    return langDicts

#Arguments:
#   listOfDicts: A list of dictionaries where the keys are n-grams and the values are the count of the n-gram
#Returns: an alphabetically sorted list containing all of the n-grams across all of the dictionaries in listOfDicts (note, do not have duplicates n-grams)
#Notes: It is recommended to use the "set" data type when doing this (look up "set union", or "set update" for python)
#   Also, for alphabetically sorted, we mean that if you have a list of the n-grams altogether across all the languages, and you call sorted() on it, that is the output we want
def dictUnion(listOfDicts):
    unionNGrams = []
    unionNGrams = set()

    for item in listOfDicts:
        unionNGrams.update(list(item.keys()))

    unionNGrams = sorted(list(unionNGrams))



    return unionNGrams


#Arguments:
#   langFiles: list of filepaths of the languages to compare testFile to.
#Returns a sorted list of all the n-grams across the languages
# Note: Use previous two functions.
def getAllNGrams(langFiles):
    allNGrams = []

    allNGrams = dictUnion(getAllDicts(langFiles))



    return allNGrams

########################################## Checkpoint, can test code above before proceeding #############################################

#Arguments:
#   testFile: mystery file's filepath to determine language of
#   langFiles: list of filepaths of the languages to compare testFile to.
#   N: the number of top n-grams for comparison
#Returns the filepath of the language that has the highest number of top 10 matches that are similar to mystery file.
#Note/Hint: depending how you implemented topNCommon() earlier, you should only need to call it once per language, and doing so avoids a possible error
def compareLang(testFile,langFiles,N):
    langMatch = ''
    topmatch = 0
    mystery = topNCommon(testFile,N)

    for path in langFiles:
        currentmatch = 0
        tmp = topNCommon(path,N)
        for check in tmp:
            for i in mystery:
                if check[0] == i[0]:
                    currentmatch +=1;
                    if currentmatch > topmatch:
                        topmatch = currentmatch
                        langMatch = path

    return langMatch




if __name__ == '__main__':
    from os import listdir
    from os.path import isfile, join, splitext
    
    #Test topNCommon()
    path = join('ngrams','english.txt')
    #print(getFormattedText('ngrams/english.txt'))
   # print(topNCommon(path,10))
    
    #Compile ngrams across all 6 languages and determine a mystery language
    path='ngrams'
    fileList = [f for f in listdir(path) if isfile(join(path, f))]
    pathList = [join(path, f) for f in fileList if 'mystery' not in f]#conditional excludes mystery.txt
    print(getAllNGrams(pathList))#list of all n-grams spanning all languages
    
    testFile = join(path,'mystery.txt')
    print(compareLang(testFile, pathList, 20))#determine language of mystery file
    
