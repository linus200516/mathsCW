import numpy as np
import math


# used to read both the doc and qurey file 
def readDoc(file_doc):
        with open(file_doc, "r") as readFile:
            docLines = readFile.readlines()
        docLines = [line.strip() for line in docLines]
        return docLines


#creation of unique words list 
def dictCreation(docs):
    #used sets due to them no allowing duplicate words
    uniqueWords = set()
    for doc in docs:
        words = doc.split()
        for word in words:
           #adding the "unique" words to the set
           uniqueWords.add(word)
    return list(uniqueWords)


#inverts index and makes a dictionary of the unique words
def invertingDict(docs, dictionary):
    #creating dictionary where each word is a key in an empty list
    invertedIndex = {word:[] for word in dictionary}
    Index = 0 
    for doc in docs:
        for word in doc.split():
            if word in invertedIndex:    
                if Index not in invertedIndex[word]:
                    invertedIndex[word].append(Index)
        Index += 1
    return invertedIndex
 

#turns doc into a vector
def documentVector(doc, dictionary):
    vector = [0] * len(dictionary)
    wordsInDoc = doc.split()
    i = 0
    for word in dictionary:
        count = wordsInDoc.count(word)
        vector[i] = count
        i+= 1 
    return vector


#uses previous function to vectorize the queries 
def queryVector(query, dictionary):
    return documentVector(query, dictionary)

##
#look at the calculating angles
##
#calculates cosine simularity 
def similarity(dVector, qVector):
    dotProduct = 0
    magnitudeD = 0
    magnitudeQ = 0

    for i in range(len(dVector)):
        dotProduct += dVector[i] * qVector[i]
        magnitudeD += dVector[i] ** 2 
        magnitudeQ += qVector[i] ** 2

    normD = np.sqrt(magnitudeD)
    normQ = np.sqrt(magnitudeQ)

    #checking if it is a norm of 0, as it is an edge case and
    #shouldn't be divided
    if normD == 0 or normQ == 0:
        return 0
    
    cosineOfTheta = dotProduct / (normD * normQ)
    
    return cosineOfTheta


#finds which docs are relevant by narrowing down the list
def findRelevantDocuments(query, docs, invertedIndex):
    #storing indicies of docs relevant to query
    relevantIds = []
    allDocsIndexes = list(range(len(docs)))
    queryWords = query.split()
    
    
    #checks to see if words from the query are in the inverted index
    for word in queryWords:
        if word in invertedIndex:
            docsWithWord = invertedIndex[word]
            if not relevantIds:  
                relevantIds = docsWithWord
            else:
                relevantIds = [docId for docId in relevantIds if docId in docsWithWord]
        else:
            return []
    
    relevantIds = [docId + 1 for docId in relevantIds]
    return relevantIds


#finds the angle between the doc vectors and query 
def calculateDocumentAngles(relevantDocs, docs, dictionary, queryVector):
    docAngles = []
    #for each document relevant doc id it calculates zero based index
    for docId in relevantDocs:
        documentIndex = docId - 1
        documentVectors = documentVector(docs[documentIndex], dictionary)
        cosineSimilarity = similarity(documentVectors, queryVector)
        #checks it is in valid range can converts to an angle
        if -1 <= cosineSimilarity <= 1 and cosineSimilarity != 0:
            angle = math.degrees(math.acos(cosineSimilarity))
            if angle < 90:
                docAngles.append((docId, angle))
    return docAngles


#formats output 
def printRelevantDocuments(docAngles):
    if docAngles:
        print("Relevant documents:", end=" ")
        for doc in docAngles:
            print(doc[0], end=" ")
        print()  
        for doc in docAngles:
            print(f"{doc[0]} {doc[1]:.5f}")
    else:
        print("No relevant documents found.")




#uses previous functions to conduct the search
def processQueries(queries, dictionary, docs, invertedIndex):
    for query in queries:
        print(f"\nQuery: {query}")
        #generating the vector 
        qVector = queryVector(query, dictionary)

        relevantDocs = findRelevantDocuments(query, docs, invertedIndex)

        docAngles = calculateDocumentAngles(relevantDocs, docs, dictionary, qVector)
        #lambda funtion to sort tuples
        docAngles.sort(key=lambda x: x[1])

        printRelevantDocuments(docAngles)




if __name__ == "__main__":
    docsFile = "docs.txt"
    queriesFile = "queries.txt"
    docs = readDoc(docsFile)
    queryFile = readDoc(queriesFile)

    dictionary = dictCreation(docs)
    invertedIndex = invertingDict(docs, dictionary)

    print(f"words in dictionary: {len(dictionary)}")
    #print(dictionary)
    #print(inverted_index)
    processQueries(queryFile, dictionary, docs, invertedIndex)