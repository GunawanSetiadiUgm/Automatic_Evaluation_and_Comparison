import re                                                           #regex, would be used to divide text into sentences
from math import *                                                  #the * so we dun need math.fung la

#unigram tokenize
def tokenizing(sentences):                                          #tokenizing sentences into list of words, for refy and candy
    helder = []                                                     #empty list, we use list to return multiple values
    for raws in range(0, len(sentences), 1):                        #iterate doc, tokenize into words
        tokens = sentences[raws].split()                            #tokens -> list of words
        helder.append(tokens)                                       #fillin the list
    return helder                                                   #return the sentences as set of words ["words1", "words2", ...]

#length of lists(candidate or reference)
def lengthmeasure(token):                                           #calculate length of each sentences(amout of words) in tokenized text
    slength = []                                                    #empty list that would be returned after filled
    for i in range(0, len(token), 1):                               #from index 0 to length of the sentence
        holder = len(token[i])                                      #set holder to length of sentence in index[i]
        slength.append(holder)                                      #fill the list
    return slength                                                  #return it

#modified unigram precision
def precision(candidates1, references1):                            #calculate the precision in a candidate sentence against a reference sentence
    count = 0                                                       #show the amount of match happened
    length = len(candidates1)                                       #the length of candidate sentence
    for i in range(0, length, 1):                                   #for each index i as long as the length of candidate....
        for j in range(0, len(references1), 1):                     #and as long as the length of reference.....
            if (candidates1[i] == references1[j]):                  #if there is a match
                candidates1[i] = ""                                 #we change candidates at index i so it won't match again next time
                references1[j] = "#"                                #same as above for the references
                count += 1                                          #because there is a match, so the count increases
    return float(count)/float(length)                               #at the end of function, we return the float(decimal) value of count/length (formula of calculating Precision)

#unigram precision in list
def list_prc(can_list, ref_list):                                   #calculate precision() in each sentences from the list of candidates against list of references
    list_Pn = []                                                    #an empty list that will be returned
    for i in range(0, len(can_list), 1):                            #for each i in the range from 0 to the length of candidate's list(amount of sentences in candidates)
        holder = precision(can_list[i], ref_list[i])                #holder calculate precision at index i sentences in between candidate and references
        list_Pn.append(holder)                                      #put each holder value in earlier empty list
    return list_Pn                                                  #return it, list of each sentences precision value

#BLEU function per sentences
def BLEUpS(prc_list):                                               #calculate BLEU in each sentences
    BLholder = []
    lengcan = lengthmeasure(candy)
    lengref = lengthmeasure(refy)
    for i in range(0, len(lengcan), 1):
        if (lengcan[i] > lengref[i]):
            Brev = 1
        else:
            Brev = exp(1 - float(lengref[i]) / lengcan[i])
        BL = Brev * exp(log10(prc_list[i]))
        BLholder.append(BL)
    print "BLEU per sentences :"
    return BLholder


#removing symbols in text and lowercasing
def neutralize(lists):
    aholder = []
    for i in range(0, len(lists), 1):
        rem_symbol = re.sub(r'[^\w]', ' ', lists[i])
        rsl = rem_symbol.lower()
        aholder.append(rsl)
    return aholder

#print each element in list
def line_print(lists2):
    for el in lists2:
        print el


#candidate = open("Kandidat_Hipotesis.txt", "r+")                                                          #open file cand
candidate = open("repair_kan.txt", "r+")
candyread = candidate.read().replace("\n"," ")                                                              #read and replace new line in .txt into a space
#reference = open("Referensi_Hipotesis.txt", "r+")                                                           #open file ref
reference = open("repair_ref.txt", "r+")
refyread = reference.read().replace("\n"," ")


uncandies = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<![A-Z][a-z][a-z]\.)(?<=\.|\?|\!)\s', candyread)
unrefies = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<![A-Z][a-z][a-z]\.)(?<=\.|\?|\!)\s', refyread)
print "Candidates :"
print ("\n".join(uncandies))
print
print "References :"
print ("\n".join(unrefies))
print

candies = neutralize(uncandies)
refies = neutralize(unrefies)

#print candies
#print refies

candy = tokenizing(candies)
line_print(candy)
c = sum(lengthmeasure(candy))
print "Number of 1-gram in each sententences: " + str(lengthmeasure(candy))
print "Total number of 1-gram in Candidate : " + str(c)
print "Total number of sentences : " + str(len(lengthmeasure(candy)))
print
refy = tokenizing(refies)
line_print(refy)
r = sum(lengthmeasure(refy))
print "Number of 1-gram in each sententences: " + str(lengthmeasure(refy))
print "Total number of 1-gram in Reference : " + str(r)
print "Total number of sentences : " + str(len(lengthmeasure(refy)))
print

Pn = list_prc(candy, refy)
print "Precision value of each sentences: " + str(Pn)
line_print(BLEUpS(Pn))
print
#Brevity Penalty
if (c > r):                                                         #in case of candy longer than refy....
    BP = 1                                                          #then this is the value of brevy
else:                                                               #in other cases,
    BP = exp(1 - float(r) / c)                                      #this is the value of brevy, it's e^()

print "Total Brevity Penalty : " + str(BP)
print

#BLEU
N = len(candy)
BLEU = BP * exp(sum(list(log10(Pn[i]) * (float(1)/N) for i in range(0, N, 1))))   #assign bleu as the formula from Mr.papineni said
#BLEU = BP * exp(sum((float(1)/N) * log10(Pn[i - 1]) for i in range(1, N, 1)))

print "Total BLEU : " + str(BLEU)                                           #so you could see the fruit of gunawan setiadi's hardwork

candidate.close()
reference.close()                                                   #codecademy teach me to always close it

