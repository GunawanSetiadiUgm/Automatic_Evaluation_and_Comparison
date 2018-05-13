import re                                                           #regex, would be used to divide text into sentences
from copy import *
from math import *                                                  #the * so we dun need math.fung la

#unigram tokenize
def tokenizing(sentences):                                          #tokenizing sentences into list of words, for refy and candy
    helder = []                                                     #empty list, we use list to return multiple values
    for raws in range(0, len(sentences), 1):                        #iterate doc, tokenize into words
        tokens = sentences[raws].split()#word_tokenize(raws)        #tokens -> list of words
        helder.append(tokens)                                       #fillin the list
    return helder                                                   #return the sentences as set of words ["words1", "words2", ...]

#length of lists(candidate or reference)
def lengthmeasure(token):                                           #calculate length of each sentences(amout of words) in tokenized text
    slength = []                                                    #empty list that would be returned after filled
    for i in range(0, len(token), 1):                               #from index 0 to length of the sentence
        holder = len(token[i])                                      #set holder to length of sentence in index[i]
        slength.append(holder)                                      #fill the list
    return slength                                                  #return it

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

def count_match(candidates1, references1):                            #calculate the precision in a candidate sentence against a reference sentence
    count = 0                                                       #show the amount of match happened
    length = len(candidates1)                                       #the length of candidate sentence
    for i in range(0, length, 1):                                   #for each index i as long as the length of candidate....
        for j in range(0, len(references1), 1):                     #and as long as the length of reference.....
            if (candidates1[i] == references1[j]):                  #if there is a match
                candidates1[i] = ""                                 #we change candidates at index i so it won't match again next time
                references1[j] = "#"                                #same as above for the references
                count += 1                                          #because there is a match, so the count increases
    return float(count)                                             #at the end of function, we return the float(decimal) value of count/length (formula of calculating Precision)

def list_match(can_list, ref_list):                                 #calculate precision() in each sentences from the list of candidates against list of references
    list_Pn = []                                                    #an empty list that will be returned
    for i in range(0, len(can_list), 1):                            #for each i in the range from 0 to the length of candidate's list(amount of sentences in candidates)
        holder = count_match(can_list[i], ref_list[i])              #holder calculate precision at index i sentences in between candidate and references
        list_Pn.append(holder)                                      #put each holder value in earlier empty list
    return list_Pn                                                  #return it, list of each sentences precision value

def print_maps(matrix):                                             #function to show the matrix of levenshtein distance
    for row in matrix:
        print "".join(str(row))
        #print row

def Levenshtein(lists1, lists2, lists3):
    length_j = len(lists1) + 2                                                                      # length of lists1, + 2 because lev dis had 2 blank startin col
    length_i = len(lists2) + 2                                                                      # length of lists2, + 2 because lev dis had 2 blank startin row
    lev = [[0 for x in range(length_j)] for y in
           range(length_i)]                                                                         # creatin matrix for levenshtein distance, default initiation is a board with 0 value

    for j in range(2, length_j):                                                                    # put refy inside first column
        lev[0][j] = lists1[j - 2]
    for i in range(2, length_i):                                                                    # put candy inside first row
        lev[i][0] = lists2[i - 2]

    start = 0                                                                                       # here lies lev[1][1]
    for i in range(1, length_i):                                                                    # for the value inside second row
        lev[i][1] = start
        start = start + 1                                                                           # increment as long as the candy
    start = 0                                                                                       # revalue lev[1][1] for second col, end up same
    for j in range(1, length_j):                                                                    # for the value inside second col
        lev[1][j] = start
        start = start + 1                                                                           # increase as long as the refy

    for i in range(2, length_i):                                                                    # formula of levenshtein distance
        for j in range(2, length_j):
            if (lev[i][0] == lev[0][j]):                                                            # read bab 3 or wikipedia
                lev[i][j] = min(lev[i][j - 1] + 1, lev[i - 1][j] + 1, lev[i - 1][j - 1])
            else:
                lev[i][j] = min(lev[i][j - 1] + 1, lev[i - 1][j] + 1, lev[i - 1][j - 1] + 1)

    leven = lev[length_i - 1][length_j - 1]                                                         # the value of last column & row, or S + D + I
    correct = lists3

    print_maps(lev)
    print "S + D + I : " + str(leven)                                                               # so you could see
    print "C : " + str(correct)
    MER = float(leven) / float(correct + leven)                                                     # the value of Match Error Rate, rate of how much the error happen
    print "MER " + str(MER)
    MAcc = 1 - MER                                                                                  # to use the same environtment (lowest/worst = 0, highest/best = 1)
    print "MAcc " + str(MAcc)                                                                       # showed another hard work of gunawan setiadi
    print

    return MAcc

def Lev_lists(candidates1, references1):
    levys = []
    for i in range(0, len(candidates1), 1):
        holders = Levenshtein(candidates1[i], references1[i], maces[i])
        levys.append(holders)
    print
    print "MAcc of each sentences "
    return levys

#candidate = open("DocKandidatTG13(hmw).txt", "r+")
candidate = open("repair_kan.txt", "r+")                          #open file cand
candyread = candidate.read().replace("\n"," ")                                #read and replace new line in .txt into a space
#reference = open("DocReferensi13(hmw).txt", "r+")
reference = open("repair_ref.txt", "r+")                           #open file ref
refyread = reference.read().replace("\n"," ")


uncandies = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<![A-Z][a-z][a-z]\.)(?<=\.|\?|\!)\s', candyread)
unrefies = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<![A-Z][a-z][a-z]\.)(?<=\.|\?|\!)\s', refyread)
print "Candidates :"
print ("\n".join(uncandies))
print
print "References :"
print ("\n".join(unrefies))
print                                                                       #show the text references that have been converted into list of sentences

candies = neutralize(uncandies)
refies = neutralize(unrefies)

candy = tokenizing(candies)                                                 #further, convert list of sentences into list of list_of_words
line_print(candy)
list_c = lengthmeasure(candy)                                               #count of words in each sentences
print "Number of 1-gram in each sententences: " + str(list_c)
print
refy = tokenizing(refies)
line_print(refy)
list_r = lengthmeasure(refy)
print "Number of 1-gram in each sententences: " + str(list_r)
print
candhold = deepcopy(candy)                                                                                              #deepcopy : we saved the current sentence's words, because some function change the text(ex : like changing words that matches between candy & refy)
refhold = deepcopy(refy)
maces = list_match(candy, refy)
print maces
candy = candhold
refy = refhold
#Levenshtein(candy[0], refy[0])
print Lev_lists(candy, refy)
#line_print(Lev_lists(candy, refy))