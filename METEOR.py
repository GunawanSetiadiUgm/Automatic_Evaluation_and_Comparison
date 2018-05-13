import re                                                           #would be used to divide text into sentences
from copy import *                                                  #we would borrow deepcopy() for restoring texts, * so we won't need copy.fung
from math import *                                                  #the * so we don't need math.fung everytime

#unigram tokenize
def tokenizing(sentences):                                          #tokenizing sentences into list of words, for refy and candy
    helder = []                                                     #empty list, we use list to return multiple values
    for raws in range(0, len(sentences), 1):                        #iterate doc, tokenize into words
        tokens = sentences[raws].split()#word_tokenize(raws)        #tokens -> list of words
        helder.append(tokens)                                       #fillin the list
    return helder                                                   #return the sentences as set of words ["words1", "words2", ...]

#removing symbols in text and lowercasing
def neutralize(lists):                                              #defining function neutralize, that remove symbols and lowercasing a list
    aholder = []                                                    #empty list as a holder
    for i in range(0, len(lists), 1):                               #loop as many as the length of the list
        rem_symbol = re.sub(r'[^\w]', ' ', lists[i])                #removing symbol
        rsl = rem_symbol.lower()                                    #lowercasing
        aholder.append(rsl)                                         #fill the holder with neutralized list
    return aholder                                                  #return the above neutralized list

#print each element in list
def line_print(lists2):                                             #defining function that print list per line
    for el in lists2:                                               #for every item inside the list
        print el                                                    #print the item

#length of lists(candidate or reference)
def lengthmeasure(token):                                           #calculate length of each sentences(amout of words) in tokenized text
    slength = []                                                    #empty list that would be returned after filled
    for i in range(0, len(token), 1):                               #from index 0 to length of the sentence
        holder = len(token[i])                                      #set holder to length of sentence in index[i]
        slength.append(holder)                                      #fill the list
    return slength                                                  #return it

#precision & recall
def precall(candidates1, references1):                              #return precision, recall, and unigram in a form of list
    listhold = []                                                   #empty list to hold value
    count = 0                                                       #count of unigram matches
    wt = len(candidates1)                                           #wt = length of candidates(used in pre)
    wr = len(references1)                                           #wr = length of references(used in rec)
    for i in range(0, wt, 1):                                       #for each index(i) as long as the length of the candidates(wt)
        for j in range(0, wr, 1):                                   #with each 2nd index(j) as long as the length of the references(wr)
            if (candidates1[i] == references1[j]):                  #we compare both candidates at [index] and references at [2nd index], in case of match :
                candidates1[i] = ""                                 #we set i to "" so that it won't match in the next iteration
                references1[j] = "#"                                #same as i we set it to # so it won't match with the later iteration
                count += 1                                          #increase the amount of unigram that mathced
    uni = count                                                     #amount of unigram matches after all those loop process
    pre = float(count)/float(wt)                                    #precision gained, float to get the decimal format of it
    rec = float(count)/float(wr)                                    #recall gained, float used same as above
    listhold.append(pre)                                            #we put pre in the list(index[0]) and
    listhold.append(rec)                                            #we put rec(index[1]) also
    listhold.append(uni)                                            #we put the uni(index[2])
    return listhold                                                 #we just return those three values as a list ([precision, recall, unigram_matches])

#uni, precision, & recalll in list
def list_prc(can_list, ref_list):                                   #this return list of precall-ed list
    list_Pn = []                                                    #empty list as usual, to return more than one value
    for i in range(0, len(can_list), 1):                            #from index 0 to length of list of candidates
        holder = precall(can_list[i], ref_list[i])                  #hold the value of precall-ing list candidates[i] with list reference[i]
        list_Pn.append(holder)                                      #append the list gained into the empty list earlier
    return list_Pn                                                  #return the list of list(list of [pre[i], rec[i], uni[i]])

#create n-gram
def ngram(lists, n, a):                                                     #define function that connects n-gram words
    holder = ""                                                             #to hold for a while
    for i in range(n, (n + a), 1):                                          #where n is the index start & a is length desired
        holder = holder + lists[i]                                          #it sums the list[i] at defined range
    return holder                                                           #return the n-gram words

#chunks
def build_chunk(candidates1, references1):                                                                              #build(actually count) number of chunks each sentence
    lstholder = []                                                                                                      #empty list, later it would return amount of chunks each sentence
    L_s = []
    L_z = []
    L_n = []
    for i in range(0, len(candidates1), 1):                                                                             #from index 0 through the length of candidates
        canori = deepcopy(candidates1[i])
        refori = deepcopy(references1[i])
        lengths = max(len(candidates1[i]), len(references1[i]))                                                         #variable that determine which one had more word(unigram) counts
        print len(candidates1[i])
        print len(references1[i])
        chunk = 0                                                                                                       #starts from 0, it would be used to count chunks. returned value
        x = 1                                                                                                           #the n value of n-gram, length of n-gram, x = 1 means it's a 1-gram
        y = 0                                                                                                           #y symbolize the index of reference
        z = 0                                                                                                           #z symbolize the index of candidates
        match = 0                                                                                                       #symbolize if there are some matches between reference and candidates(1 means a unigram matches/chunk, 2 means a bigram matches/chunk, and so on)
        while (z + x) <= lengths and z <= len(candidates1[i]):                                                          # the condition that means it isn't the end of candidate sentence, we used {while} to change index flexibly
            if ((z + x) >= len(candidates1[i]) and (y + x) >= len(references1[i])):                                     # if z + x is longer than length of candy
                if (match > 0):                                                                                         # i've had explained it at the first condition above, should've made it into a function. From here.....
                    mat = deepcopy(match)
                    L_n.append(mat)
                ios = 0
                while (len(L_n) > 0):
                    q = L_n.index(max(L_n))
                    if (max(L_n) > 1 and L_s[q] + L_n[q] != ios and references1[i][L_s[q]] == candidates1[i][L_z[q]]):
                        ios = L_s[q] + L_n[q]
                        for o in range(L_s[q], (L_s[q] + L_n[q]), 1):
                            references1[i][o] = "*"
                        for r in range(L_z[q], (L_z[q] + L_n[q]), 1):
                            candidates1[i][r] = "#"
                        del L_s[q]
                        del L_z[q]
                        del L_n[q]
                        chunk = chunk + 1
                    elif (L_s[q] + L_n[q] == ios):
                        del L_s[q]
                        del L_z[q]
                        del L_n[q]
                    elif (max(L_n) > 1 and L_s[q] + L_n[q] != ios):
                        del L_s[q]
                        del L_z[q]
                        del L_n[q]
                    elif (max(L_n) == 1 and references1[i][L_s[q]] == candidates1[i][L_z[q]]):
                        references1[i][L_s[q]] = "*"
                        candidates1[i][L_z[q]] = "#"
                        chunk = chunk + 1
                        del L_s[q]
                        del L_z[q]
                        del L_n[q]
                    else:
                        del L_s[q]
                        del L_z[q]
                        del L_n[q]
                break                                                                                                   # break out from the while, cause it's the end of candidate's sentence
            elif ((z + x) >= len(candidates1[i]) and (y + x) < len(references1[i])):
                y = y + x
                x = 1
            elif (y + x >= (lengths + 1)):                                                                              # it means a chunk has been completed(reference couldn't get any longer), thus point the next index. Not possible on the first iteration
                if (match > 0):                                                                                         # another condition to fulfill, logically if there is no match then there ain't any chunk created
                    mat = deepcopy(match)
                    L_n.append(mat)
                    match = 0                                                                                           # we reset the match into 0 once more
                if (x == 1):                                                                                            # another condition, if it's a unigram
                    z = z + x                                                                                           # then we increase candidate index(z) by 1
                elif (x > 1):                                                                                           # but if it's longer than a unigram
                    z = z + (x - 1)                                                                                     # z increase by the value of n in n-gram minus 1
                x = 1                                                                                                   # reset x to 1-gram
                y = 0                                                                                                   # start iterating from first refy (per 1-gram) again
                print ((z, x), (y, x))                                                                                  # just for showing the index,n-gram of candidates(z,x) and references(y,x)
            elif (y + x >= len(references1[i]) + 1):                                                                    # if the current refy index + n of n-gram is greater or equal the length of references + 1
                if (match > 0):                                                                                         # i've had explained it at the first condition above, should've made it into a function. From here.....
                    mat = deepcopy(match)
                    L_n.append(mat)
                    match = 0
                if (x == 1):
                    z = z + x
                elif (x > 1) :
                    z = z + (x - 1)                                                                                     #.....till here(till the end of this "if", actually) same as first condition above
                x = 1                                                                                                   # this whole elif works if we reach last word of refy, thus we reset to 1-gram
                y = 0                                                                                                   # we reset the index of refy as well(y = 0)
                print ((z, x), (y, x))                                                                                  # current index of candy and refy
            elif (ngram(candidates1[i], z, x) == ngram(references1[i], y, x)):                                          # comparin if n-gram at sentences[i] in candidates and references is a match...
                if (x == 1):                                                                                            # if it's still a unigram(x equal 1), then
                    zi = deepcopy(z)
                    L_z.append(zi)
                    why = deepcopy(y)                                                                                   # copy/save references index(y), symbolize the index of first match happened
                    L_s.append(why)
                print ngram(references1[i], y, x)                                                                       # print the word
                match = match + 1                                                                                       # record unigram series matches (match = 1, means a unigram and so on...)
                x = x + 1                                                                                               # ...the next word might be a match as well!(as n-gram)
            else:                                                                                                       # if those previous "if" condition didn't fulfill....
                if(match > 0):
                    y = y + 1
                    x = 1
                    mat = deepcopy(match)
                    L_n.append(mat)
                    match = 0
                else:
                    print ((z, x), (y, x))                                                                              # show at which point of index
                    y = y + 1                                                                                           # refy index + 1, next word in reference
        print "final chunk: " + str(chunk)                                                                              # show the final amount of chunks gained
        candidates1[i] = canori
        references1[i] = refori
        print candidates1[i]
        print references1[i]
        lstholder.append(chunk)                                                                                         # append the chunks gained, we would return multiple of it
    print "number of chunk in each sentences: "
    return lstholder                                                                                                    # return list of number of chunks each sentence had

#METEOR
def METEOR(precalls1, chunks1):                                             # METEOR function, inputs are precalled list and list of their chunks
    list_mtr = []                                                           # we would return list of each METEOR values
    for k in range(0, len(precalls1), 1):                                   # from index 0 to length of precalled list
        P = precalls1[k][0]                                                 # we set Precision(P) it's in index[0] of each list
        R = precalls1[k][1]                                                 # we set Recall(R) it's in index[1] of each list
        match = precalls1[k][2]                                             # we set Unigram matches(match) it's in index[2] of each list

        print "Precision: " + str(P)                                        # print Precision
        print "Recall : " + str(R)                                          # print Recall
        print "unigram match: " + str(match)                                # print Unigram matches
        if P > 0 and R > 0:                                                 # if there is value of P and R
            Fmean = (10 * P * R) / (9 * P + R)                              # we calculate through the theorem to get Fmean
        else:                                                               # if there isn't any value of P and R(no match at all!)
            Fmean = 0                                                       # then we set Fmean to 0, to avoid zero division(0/0)

        print "Fmean: " + str(Fmean)                                        # print Fmean, what else?

        if match > 0:                                                       # if there is any match
            penalty = 0.5 * (float(chunks1[k]) / float(match)) ** 3         # calculate the penalty
        else:                                                               # no match at all
            penalty = 0                                                     # again to avoid zero div

        print "penalty: " + str(penalty)                                    # amount of penalty gained
        print                                                               # everybody needs some space
        M = Fmean * (1 - penalty)                                           # METEOR formula
        list_mtr.append(M)                                                  # append the METEOR value gained
    print "METEOR Scores: "
    return list_mtr                                                         # finally we return the list of METEOR values per sentence of the text


#candidate = open("DocKandidatTG13(hmw).txt", "r+")                                                                      #open file cand, "r+" means we read and used it's value
candidate = open("repair_kan.txt", "r+")
candyread = candidate.read().replace("\n"," ")                                                                          #read the candidate, thus we gained the raw text/corpora/phrase
#reference = open("DocReferensi13(hmw).txt", "r+")                                                                       #open file ref, "r+" means we read and used it's value
reference = open("repair_ref.txt", "r+")
refyread = reference.read().replace("\n"," ")                                                                           #read the reference, thus we gained the raw text/corpora/phrase

uncandies = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<![A-Z][a-z][a-z]\.)(?<=\.|\?|\!)\s', candyread)                   #split the text into list of sentences, explanation of regex at documentation
unrefies = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<![A-Z][a-z][a-z]\.)(?<=\.|\?|\!)\s', refyread)                     #split the text into list of sentences, explanation of regex at documentation
print "Candidates :"
print ("\n".join(uncandies))                                                                                            #show the text candidates that have been converted into list of sentences
print
print "References :"
print ("\n".join(unrefies))                                                                                             #show the text references that have been converted into list of sentences
print
candies = neutralize(uncandies)                                                                                         #neutralize remove symbols and lowercasing text, it's necessary so that a word with . still match with the one without
refies = neutralize(unrefies)
print "parsed into unigram :"
candy = tokenizing(candies)                                                                                             #further, convert list of sentences into list of list_of_words
line_print(candy)
list_c = lengthmeasure(candy)                                                                                           #count of words in each sentences
print "Number of 1-gram in each sententences: " + str(list_c)
print
refy = tokenizing(refies)
line_print(refy)
list_r = lengthmeasure(refy)
print "Number of 1-gram in each sententences: " + str(list_r)

candhold = deepcopy(candy)                                                                                              #deepcopy : we saved the current sentence's words, because some function change the text(ex : like changing words that matches between candy & refy)
refhold = deepcopy(refy)
print
chunky = build_chunk(candy, refy)                                                                                       #we count the chunk between parameters, those are candy & refy
print chunky
print
candy = candhold                                                                                                        #the text had been changed as a result of the function before, so we change it back with a variable that holds the deepcopy
refy = refhold

PRmatch = list_prc(candy, refy)                                                                                         #create the list of precall(precision, recall, and unigram match) based on the candy & refy
print "Precision, Recall, and 1-gram matches in each sentence: " + str(PRmatch)                                         #print it

print
#print str(METEOR(PRmatch, chunky))
line_print(METEOR(PRmatch, chunky))                                                                  #print METEOR Scores, complete with Precision, Recall, Unigram_match, F-mean, and penalty of each Sentences

candy = candhold                                                                                                        #once more, the text had been changed as a result of the function before, so we change it back with a variable that holds the deepcopy
refy = refhold
candidate.close()
reference.close()
