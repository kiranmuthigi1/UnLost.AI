from keras import backend as K
K.set_image_data_format('channels_first')
import sys
from fr_utils import *
from inception_blocks_v2 import *
import os
from os.path import join
import numpy as np
import pickle

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

def check_func(argum1):

    np.set_printoptions(threshold=sys.maxsize)
    print("inside: ", argum1)
    FRmodel = faceRecoModel(input_shape=(3, 96, 96))
    lost = '/home/zemotacqy/hack-moscow-backend/routes/../uploads/lost'
    print("lost FilePath: ", lost)
    files= os.listdir(lost)
    print(files)
    #sys.stdout.flush()
    FRmodel.compile(optimizer='adam', loss=triplet_loss, metrics=['accuracy'])
    print("Loading weitghts:")
    load_weights_from_FaceNet(FRmodel)
    cur_encoding = img_to_encoding(argum1, FRmodel)
    print(cur_encoding)
    #sys.stdout.flush()
    check = 0
    best_match_found = ""
    cur_b_sc= 0.7
    for i in files:
        fadd = join(lost,i)
        imgs2 = os.listdir(fadd)
        imgs = []
        for file in imgs2:
            if file.endswith(".pkl"):
                imgs.append(file)
        for j in imgs:
            with open(join(fadd,j), 'rb') as f:
                val = pickle.load(f)
            dist = np.linalg.norm(np.subtract(cur_encoding, val))
            if dist<cur_b_sc:
                cur_b_sc = dist
                check = 1
                best_match_found = i
    if(check==1):
        print(best_match_found)
        print(cur_b_sc)
        sys.stdout.flush()
    else:
        print("NULL")
        print("NULL")
        sys.stdout.flush()

if __name__=="__main__":
    argument1 = sys.argv[1]
    check_func(argument1)




