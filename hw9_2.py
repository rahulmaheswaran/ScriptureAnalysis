
from helper import remove_punc
import numpy as np
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer


#Clean and stem the contents of a document
#Takes in a file name to read in and clean
#Return a list of words, without stopwords and punctuation, and with all words stemmed
# NOTE: Do not append any directory names to doc -- assume we will give you
# a string representing a file name that will open correctly
def readAndCleanDoc(doc):
    #1. Open document, read text into *single* string
    with open(doc,"r") as myfile:
        corpus = myfile.read()

    #2. Tokenize string using nltk.tokenize.word_tokenize
    doc_tokens = nltk.tokenize.word_tokenize(corpus)

    #3. Filter out punctuation from list of words (use remove_punc)
    doc_tokens_no_punc = remove_punc(doc_tokens)

    #4. Make the words lower case
    doc_tokens_lower = [x.lower() for x in doc_tokens_no_punc]

    #5. Filter out stopwords
    stop = stopwords.words('english')
    words = [x for x in doc_tokens_lower if x not in stop]


    #6. Stem words
    stemmer = PorterStemmer()
    #lemmatizer = WordNetLemmatizer()
    words = [stemmer.stem(x) for x in words]

    return words
    
#Builds a doc-word matrix for a set of documents
#Takes in a *list of filenames*
#
#Returns 1) a doc-word matrix for the cleaned documents
#This should be a 2-dimensional numpy array, with one row per document and one 
#column per word (there should be as many columns as unique words that appear
#across *all* documents. Also, Before constructing the doc-word matrix, 
#you should sort the wordlist output and construct the doc-word matrix based on the sorted list
#
#Also returns 2) a list of words that should correspond to the columns in
#docword
def buildDocWordMatrix(doclist) :
    #1. Create word lists for each cleaned doc (use readAndCleanDoc)
    tmp = []
    wordlist = []
    #get all the words from all files
    for doc in doclist:
        tmp.append(readAndCleanDoc(doc))
    for dlist in tmp:
        for word in dlist:
            if(not(word in wordlist)):
                wordlist.append(word)

    wordlist = sorted(wordlist)

    docword = np.zeros((len(doclist), len(wordlist)))
    for ind, wordL in enumerate(tmp):
        for word in wordL:
            docword[ind,wordlist.index(word)] +=1
    return docword, wordlist


    #Create Word_List dict, where {doc: list of words}

'''
    word_to_ind = {word: ind for ind, word in enumerate(word_list)}
    
    for doc, doc_vec in zip(word_list, doc_word):
        for word in doc:
            ind = word_to_ind[word]
            doc_vec[ind] += 1
            '''


    #2. Use these word lists to build the doc word matrix
    #word_list = d = dict(itertools.zip_longest(*[iter(wordlist)] * 2, fillvalue=""))
'''
    # Then, construct the bag-of-words representation of each document
    doc_word= []
    for doc in doclist:
        doc_vec = [0] * len(wordlist)  # Each document is represented as a vector of wordoccurrences
    for word in doc:
        ind = wordlist.index(word)
    doc_vec[ind] += 1  # Increment the corresponding word index
    doc_word.append(doc_vec)
    return docword, wordlist


word_list = {i: "pygame.image.load({})".format(x) for i, x in enumerate(wordlist)}
    word_ind = {word:ind for ind, word in enumerate(word_list)}
    docword = np.zeros((len(doclist), len(wordlist)))
    for doc, doc_vec in zip(doclist, docword):
        for word in doc:
            ind = word_ind[word]
        doc_vec[ind] += 1
'''

            

    
#Builds a term-frequency matrix
#Takes in a doc word matrix (as built in buildDocWordMatrix)
#Returns a term-frequency matrix, which should be a 2-dimensional numpy array
#with the same shape as docword
def buildTFMatrix(docword) :
    #fill in
    tf = []
    for row in range(0,len(docword)):
        total = 0
        tf.append([])
        for col in range(len(docword[row])):
            total = total+docword[row][col]
        for col in range(len(docword[row])):
            tf[row].append(docword[row][col]/total)
    tf = np.asarray(tf)
    return tf
    
#Builds an inverse document frequency matrix
#Takes in a doc word matrix (as built in buildDocWordMatrix)
#Returns an inverse document frequency matrix (should be a 1xW numpy array where
#W is the number of words in the doc word matrix)
#Don't forget the log factor!
def buildIDFMatrix(docword) :
    #fill in

    idf = []
    for i in range(0,len(docword[0])):
        j = 0
        for k in range(0,len(docword)):
            if docword[k][i] > 0:
                j +=1

        idf.append(np.log10(len(docword)/j))
    idf = np.asarray(idf)
    idf = idf.reshape(1,-1)

    return idf
    
#Builds a tf-idf matrix given a doc word matrix
def buildTFIDFMatrix(docword) :
    #fill in
    tfidf = np.multiply(buildTFMatrix(docword),buildIDFMatrix(docword))


    return tfidf
    
#Find the three most distinctive words, according to TFIDF, in each document
#Input: a docword matrix, a wordlist (corresponding to columns) and a doclist 
# (corresponding to rows)
#Output: a dictionary, mapping each document name from doclist to an (ordered
# list of the three most common words in each document
def findDistinctiveWords(docword, wordlist, doclist) :
    distinctiveWords = {}
    #fill in
    #you might find numpy.argsort helpful for solving this problem:
    #https://docs.scipy.org/doc/numpy/reference/generated/numpy.argsort.html

    tfidf = buildTFIDFMatrix(docword)


    for i in range(0,len(doclist)):
        tmp1 = []
        tmp2 = []
        newtfidf = np.argsort(-tfidf[i])
        for k in range(0,3):
            tmp1.append(newtfidf[k])
        for l in tmp1:
            tmp2.append(wordlist[l])

        distinctiveWords[doclist[i]] = np.array(tmp2)


    
    
    return distinctiveWords


if __name__ == '__main__':
    from os import listdir
    from os.path import isfile, join, splitext
    
    ### Test Cases ###
    directory='lecs'
    path1 = join(directory, '1_vidText.txt')
    path2 = join(directory, '2_vidText.txt')
    
    # Uncomment and recomment ths part where you see fit for testing purposes

    print("*** Testing readAndCleanDoc ***")
    print(readAndCleanDoc(path1)[0:5])

    print("*** Testing buildDocWordMatrix ***") 
    doclist =[path1, path2]
    docword, wordlist = buildDocWordMatrix(doclist)
    print(docword.shape)
    print(len(wordlist))
    print(docword[0][0:10])
    print(wordlist[0:10])
    print(docword[1][0:10])

    print("*** Testing buildTFMatrix ***") 
    tf = buildTFMatrix(docword)
    print(tf[0][0:10])
    print(tf[1][0:10])
    print(tf.sum(axis =1))
    print("*** Testing buildIDFMatrix ***")

    idf = buildIDFMatrix(docword)
    print(idf[0][0:10])
    print("*** Testing buildTFIDFMatrix ***") 
    tfidf = buildTFIDFMatrix(docword)
    print(tfidf.shape)
    print(tfidf[0][0:10])
    print(tfidf[1][0:10])
    print("*** Testing findDistinctiveWords ***")
    print(findDistinctiveWords(docword, wordlist, doclist))
