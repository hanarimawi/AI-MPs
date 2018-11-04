# viterbi.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Renxuan Wang (renxuan2@illinois.edu) on 10/18/2018
import numpy as np
import math
"""
This is the main entry point for MP5. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

'''
TODO: implement the baseline algorithm.
input:  training data (list of sentences, with tags on the words)
        test data (list of sentences, no tags on the words)
output: list of sentences, each sentence is a list of (word,tag) pairs.
        E.g., [[(word1, tag1), (word2,   tag2)], [(word3, tag3), (word4, tag4)]]
'''
def process_word(word):
    word = word.replace('``', '')
    # word = word.lower()
    return word

def baseline(train, test):
    freq = {}
    pos = {}
    for sentence in train:
        for word in sentence:
            word = (process_word(word[0]), word[1])
            if word[1] in pos:
                pos[word[1]]+=1
            else:
                pos[word[1]]=1

            if word[0] in freq.keys():
                if word[1] in freq[word[0]].keys():
                    freq[word[0]][word[1]]+=1
                else:
                    freq[word[0]][word[1]] = 1
            else:
                freq[word[0]]= {}
                freq[word[0]][word[1]] = 1
    # print(pos)

    highest_frequency = 0
    best_guess= ''
    for tag in pos:
        if pos[tag]>highest_frequency:
            best_guess = tag
            highest_frequency = pos[tag]

    ind = 0
    predicts = []
    for sentence in test:
        predicts.append([])
        for word in sentence:
            word = process_word(word)
            if word in freq.keys():
                max = 0
                for tag in freq[word].keys():
                    if freq[word][tag] > max:
                        best = tag
                        max = freq[word][tag]
            else:
                #print(word[0])
                best = best_guess
            predicts[ind].append((word, best))
        ind+=1


    return predicts

'''
TODO: implement the Viterbi algorithm.
input:  training data (list of sentences, with tags on the words)
        test data (list of sentences, no tags on the words)
output: list of sentences with tags on the words
        E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
'''
def normalize(dic, a):
    count = 0
    for key in dic:
        dic[key]+=a
        count+=dic[key]
    for key in dic:
        dic[key] /= count
        dic[key] = math.log(dic[key])
    return dic

def viterbi(train, test):
    freq = {}
    pos = {} #state observation likelihood dic - each tag is a key to a dic that has word counts for that tag
    initial = {} #initial probability dic- counts # of times each tag is seen at the start of a sentence
    trans = {} #transition probability dic - tracks consecutive tag counts
    tags = set()
    for sentence in train:

        if sentence == []:
            continue

        #calc initial probabilities
        first = sentence[0]
        if first[1] in initial.keys():
            initial[first[1]]+=1
        else:
            initial[first[1]]=1

        #handle transition probabilities
        prev = ()
        for word in sentence:
            word = (process_word(word[0]), word[1])

            if word in pos:
                pos[word]+=1
            else:
                pos[word]=1

            if prev == ():
                prev = word
                continue
            else:
                if (prev[1],word[1]) in trans:
                    trans[(prev[1],word[1])]+=1
                else:
                    trans[(prev[1],word[1])]=1
    for key in trans.keys():
        tags.add(key[0])
        tags.add(key[1])
    tags = list(tags)
    trans['unknown'] = 0
    pos['unknown'] = 0
    trans = normalize(trans,1)
    pos = normalize(pos,1)
    initial = normalize(initial,0)
    #print(initial_counts)
    #print(c)
    predicts = []
    for sentence in test:
        if not sentence:
            predicts.append([])
            continue
        trellis = np.zeros((len(sentence), len(tags)))
        for i in range(len(tags)):
            word = process_word(sentence[0])
            if (word, tags[i]) in pos:
                p_emission = pos[(word, tags[i])]
            else:
                p_emission = pos['unknown']
            trellis[0][i] = initial[tags[i]] + p_emission
        backtrack = np.zeros((len(sentence), len(tags)))
        for i in range(1, len(sentence)):
            word = process_word(sentence[i])
            for j in range(len(tags)):
                best_val = -99999
                best_tag = None
                for k in range(len(tags)):
                    if (tags[k],tags[j]) in trans:
                        p_transition = trans[(tags[k],tags[j])]
                    else:
                        p_transition = trans['unknown']
                    if (word, tags[j]) in pos:
                        p_emission = pos[(word, tags[j])]
                    else:
                        p_emission = pos['unknown']
                    # print(p_transition, p_emission)
                    temp = p_transition + p_emission + trellis[i-1][k]
                    if temp > best_val:
                        best_val = temp
                        best_tag = k
                trellis[i][j] = best_val
                backtrack[i][j] = best_tag
        chain = []
        for i in range(1,len(sentence)+1):
            word = process_word(sentence[len(sentence)-i])
            l = list(trellis[len(sentence)-i])
            chain.insert(0, (word,tags[l.index(max(l))]))
        predicts.append(chain)

    #print(trans)


    return predicts
