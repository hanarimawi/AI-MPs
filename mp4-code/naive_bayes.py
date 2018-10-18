# naive_bayes.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 09/28/2018

"""
This is the main entry point for MP4. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

def naiveBayes(train_set, train_labels, dev_set, smoothing_parameter):
    """
    train_set - List of list of words corresponding with each email
    example: suppose I had two emails 'i like pie' and 'i like cake' in my training set
    Then train_set := [['i','like','pie'], ['i','like','cake']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two emails, first one was spam and second one was ham.
    Then train_labels := [0,1]

    dev_set - List of list of words corresponding with each email that we are testing on
              It follows the same format as train_set

    smoothing_parameter - The smoothing parameter you provided with --laplace (1.0 by default)
    """
    # do some data cleaning on the training set and the dev set before we start (optional, test if needed)

    # get word counts of each class
    count_spam = {}
    count_ham = {}
    num_words_ham = 0
    num_words_spam = 0
    for email in range(len(train_set)):
        doc_class = train_labels[email]
        for word in train_set[email]:
            if doc_class == 0:
                if word not in count_spam:
                    count_spam[word] = 1
                    num_words_spam += 1
                else:
                    count_spam[word] += 1
                    num_words_spam += 1
            elif doc_class == 1:
                if word not in count_ham:
                    count_ham[word] = 1
                    num_words_ham += 1
                else:
                    count_ham[word] += 1
                    num_words_ham += 1

    # setup constants for our log likelihood calculation
    log_likelihood_ham = {}
    log_likelihood_spam = {}
    types_of_words_ham = len(count_ham)
    types_of_words_spam = len(count_spam)
    log_likelihood_ham["UNKNOWN"] = smoothing_parameter / (num_words_ham + (smoothing_parameter*(types_of_words_ham+1)))
    log_likelihood_spam["UNKNOWN"] = smoothing_parameter / (num_words_spam + (smoothing_parameter*(types_of_words_spam+1)))

    # calculate log likelihoods for each type of word
    for word in count_ham:
        log_likelihood_ham[word] = (count_ham[word] + smoothing_parameter) \
                                   / (num_words_ham + (smoothing_parameter*(types_of_words_ham+1)))
    for word in count_spam:
        log_likelihood_spam[word] = (count_ham[word] + smoothing_parameter) \
                              / (num_words_spam + (smoothing_parameter*(types_of_words_spam+1)))

    # return predicted labels of development set
    return []
