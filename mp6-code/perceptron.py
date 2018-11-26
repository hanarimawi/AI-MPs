# perceptron.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/27/2018

import numpy as np

"""
This is the main entry point for MP6. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

def classify(train_set, train_labels, dev_set, learning_rate,max_iter):
    """
    train_set - A Numpy array of 32x32x3 images of shape [7500, 3072].
                This can be thought of as a list of 7500 vectors that are each
                3072 dimensional.  We have 3072 dimensions because there are
                each image is 32x32 and we have 3 color channels.
                So 32*32*3 = 3072
    train_labels - List of labels corresponding with images in train_set
    example: Suppose I had two images [X1,X2] where X1 and X2 are 3072 dimensional vectors
             and X1 is a picture of a dog and X2 is a picture of an airplane.
             Then train_labels := [1,0] because X1 contains a picture of an animal
             and X2 contains no animals in the picture.

    dev_set - A Numpy array of 32x32x3 images of shape [2500, 3072].
              It is the same format as train_set
    """
    bias_column_train = np.ones((train_set.shape[0], 1))
    train = np.concatenate((train_set, bias_column_train), axis=1)
    bias_column_dev = np.ones((dev_set.shape[0], 1))
    dev = np.concatenate((dev_set, bias_column_dev), axis=1)
    weights = np.zeros(train.shape[1])

    for epoch in range(max_iter):
        for image_index in range(train_set.shape[0]):
            funcX = np.dot(train[image_index], weights)
            prediction = True
            if funcX < 0:
                prediction = False
            if prediction != train_labels[image_index]:
                multiplier = -1
                if train_labels[image_index]:
                    multiplier = 1
                weights += (learning_rate * multiplier * train[image_index])

    dev_labels = []
    for image in dev:
        funcX = np.dot(image, weights)
        if funcX > 0:
            dev_labels.append(True)
        else:
            dev_labels.append(False)
    return dev_labels



from numpy import linalg as LA
def getDistance(image1, image2):
	return abs(LA.norm(image1 - image2, 1))

import operator 
def getNeighbors(trainingSet, testimage, k):
	distances = []
	for x in range(len(trainingSet)):
		dist = getDistance(testimage, trainingSet[x])
		distances.append((x, dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors #indices

def getPrediction(neighbors):
    return np.mean(neighbors) > 0.5

def classifyEC(train_set, train_labels, dev_set,learning_rate,max_iter):

    k = 3
    dev_labels = []
    for image_index in range(dev_set.shape[0]):
        kNN = getNeighbors(train_set, dev_set[image_index], k)
        neighbor_labels = []
        for neighbor in kNN:
            neighbor_labels.append(train_labels[neighbor])
        result = getPrediction(neighbor_labels)
        dev_labels.append(result)
    print("k=", k)
    return dev_labels