from keras import backend as K
K.set_image_data_format('channels_first')
import sys
from fr_utils import *
from inception_blocks_v2 import *
import os
from os.path import join
import numpy as np
import pickle
from pymongo import MongoClient
from pprint import pprint

def triplet_loss(y_true, y_pred, alpha=0.2):
    anchor, positive, negative = y_pred[0], y_pred[1], y_pred[2]

    # Step 1: Compute the (encoding) distance between the anchor and the positive, you will need to sum over axis=-1
    pos_dist = tf.reduce_sum(tf.square(tf.subtract(anchor, positive)), axis=-1)
    # Step 2: Compute the (encoding) distance between the anchor and the negative, you will need to sum over axis=-1
    neg_dist = tf.reduce_sum(tf.square(tf.subtract(anchor, negative)), axis=-1)
    # Step 3: subtract the two previous distances and add alpha.
    basic_loss = tf.add(tf.subtract(pos_dist, neg_dist), alpha)
    # Step 4: Take the maximum of basic_loss and 0.0. Sum over the training examples.
    loss = tf.reduce_sum(tf.maximum(basic_loss, 0.0))

    return loss

def createEmbed(argum1,FRmodel):

    np.set_printoptions(threshold=sys.maxsize)
    #print("DSf")
    files= os.listdir(argum1)
    for i in files:
        fadd = join(argum1,i)
        mylist = img_to_encoding(fadd,FRmodel)

        with open(join(argum1, i.replace('jpg','pkl')), 'wb') as f:
            pickle.dump(mylist, f)

if __name__=="__main__":
    #argument1 = sys.argv[1]
    # Argumnet is the name of folder
    client = MongoClient("mongodb://localhost/moscow")
    db=client.mongo
    serverStatusResult=db.command("serverStatus")
    db = client.moscow
    collection = db.losts
    FRmodel = faceRecoModel(input_shape = (3,96,96))
    FRmodel.compile(optimizer='adam',loss=triplet_loss,metrics=['accuracy'])
    load_weights_from_FaceNet(FRmodel)
    for document in collection.find({"isEncoding": False}):
        #print("/home/zemotacqy/hack-moscow-backend/uploads/lost/"+document["label"])
        createEmbed("/home/zemotacqy/hack-moscow-backend/uploads/lost/"+document["label"],FRmodel)
        collection.update_one({"label":document["label"]}, {"$set": {"isEncoding": True}})
    
    print("Done")



