# viterbi.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Renxuan Wang (renxuan2@illinois.edu) on 10/18/2018
import numpy as np
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
        E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
'''
def process_word(word):
    word = word.replace('``', '')
    word = word.lower()
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
    print(pos)

    highest_frequency = 0
    best_guess= ''
    for tag in pos:
        if pos[tag]>highest_frequency:
            best_guess = tag
            highest_frequency = pos[tag]

    ind = 0
    print(test)
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
def viterbi(train, test):
    predicts = []
    return predicts
