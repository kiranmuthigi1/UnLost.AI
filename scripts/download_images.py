#!/usr/bin/env python
'''

Reddit Image Downloader

Usage: download_images.py [-s SUBREDDIT] [-n NUMBER OF PICTURES] [-p PAGE] [-q SEARCH QUERY] 

-h --help                           show this
-s --subreddit SUBREDDIT            specify subreddit
-n --number NUMBER OF PICTURES      specify number of pictures to download [default: 20]
-p --page PAGE                      hot, top, controversial, new, rising [default: hot]
-q --query SEARCH QUERY             specify a specific search term

'''

import praw
import urllib.request
import sys
import os
import signal
from credentials import ID, SECRET, PASSWORD, AGENT, USERNAME
from prawcore import NotFound
from prawcore import PrawcoreException
from docopt import docopt
import cv2

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

def main():
    # initialize variables
	variable  = sys.argv[1]


    FRmodel = faceRecoModel(input_shape=(3, 96, 96))
    FRmodel.compile(optimizer='adam', loss=triplet_loss, metrics=['accuracy'])
    load_weights_from_FaceNet(FRmodel)
    variable_embedding  = img_to_encoding(variable, FRmodel)
    subreddit = ''
    num_pics = 0
    cur_b_sc = 0.7
    check = 0

    # handle 'ctrl + c' if downloads takes too long
    def sigint_handler(signum, frame):
        print ('\nQuitting...')
        sys.exit(1)

    signal.signal(signal.SIGINT, sigint_handler)

    # connect to reddit
    reddit = praw.Reddit(
        client_id=ID,
        client_secret=SECRET,
        password=PASSWORD,
        user_agent=AGENT,
        username=USERNAME)

    # get values of arguments
    subreddit = 'random' #arguments.get('--subreddit')
    num_pics = 1000 #int(arguments.get('--number'))
    search_term = arguments.get('--query')
    page = arguments.get('--page')

    for i in range (10000):

        # prompt for a subreddit if none given
	    if subreddit == None:
	        while True:
	            # obtain subreddit to download images from, and number of images to download
	            subreddit = input('Please enter subreddit: ')

	            # check that subreddit exists
	            try:
	                reddit.subreddits.search_by_name(subreddit, exact=True)
	                break
	            except NotFound:
	                print ('Subreddit %s does not exist.' % subreddit)

	    # determine what to search
	    if search_term == None:
	        if page == 'hot':
	            results = reddit.subreddit(subreddit).hot()
	        elif page == 'controversial':
	            results = reddit.subreddit(subreddit).controversial()
	        elif page == 'top':
	            results = reddit.subreddit(subreddit).top()
	        elif page == 'rising':
	            results = reddit.subreddit(subreddit).rising()
	        elif page == 'new':
	            results = reddit.subreddit(subreddit).new()
	    else:
	        results = reddit.subreddit(subreddit).search(
	            search_term, params={'nsfw': 'yes'})

	    # create images folder if one does not exits
	    if not os.path.exists('./images'):
	        os.mkdir('./images')

	    # find images/gifs in subreddit
	    try:
	        count = 1
	        for submission in results:
	            if count <= num_pics:
	                if 'https://i.imgur.com/' in submission.url or 'https://i.redd.it' in submission.url:
	                    img_url = submission.url
	                    _, extension = os.path.splitext(img_url)
	                    if extension in ['.jpg', '.jpeg']:
	                        print ('\nDownloading', subreddit + str(
	                            count) + extension)
	                        print ('Source:', img_url)
	                        print ('Comments: https://www.reddit.com/r/' + subreddit + '/comments/' + str(
	                            submission))
	                        urllib.request.urlretrieve(img_url, 'images/%s%i%s' %
	                                           (subreddit, count, extension))
	                        #img = cv2.imread ('images/%s%i%s' %
	                        #                   (subreddit, count, extension))
	                        #whatever siamese network does
                            mylist = img_to_encoding('images/%s%i%s' % (subreddit, count, extension), FRmodel)
                            dist = np.linalg.norm(np.subtract(variable_embedding, mylist))
                            if dist < cur_b_sc:
                                cur_b_sc = dist
                                check = 1
                                best_match_found = img_url
	                        os.remove ('images/%s%i%s' %
	                                           (subreddit, count, extension))
	                        count += 1
	                    # .gifv file extensions do not play, convert to .gif
	                    elif extension == '.gifv':
	                        print ('\nDownloading', subreddit + str(count) + '.gif')
	                        print ('Source:', img_url)
	                        print ('Comments: https://www.reddit.com/r/' + subreddit + '/comments/' + str(
	                            submission))
	                        root, _ = os.path.splitext(img_url)
	                        img_url = root + '.gif'
	                        urllib.urlretrieve(img_url, 'images/%s%i%s' %
	                                           (subreddit, count, '.gif'))
	                        img = cv2.imread ('images/%s%i%s' %
	                                           (subreddit, count, extension))
	                        #whatever siamese network does

	                        os.remove ('images/%s%i%s' %
	                                           (subreddit, count, extension))
	                        count += 1
	                if 'https://thumbs.gfycat.com/' in submission.url:
	                    img_url = submission.url
	                    print ('\nDownloading', subreddit + str(count) + '.gif')
	                    print ('Source:', img_url)
	                    print ('Comments: https://www.reddit.com/r/' + subreddit + '/comments/' + str(
	                        submission))
	                    urllib.urlretrieve(img_url, 'images/%s%i%s' %
	                                       (subreddit, count, '.gif'))
	                    os.remove ('images/%s%i%s' %
	                                           (subreddit, count, '.gif'))
	                    count += 1
	                # some gfycat conversions will not work due to capitalizations of link
	                if 'https://gfycat.com/' in submission.url:
	                    img_url = submission.url
	                    img_url = img_url.split('https://', 1)
	                    img_url = 'https://thumbs.' + img_url[1]
	                    if 'gifs/detail/' in img_url:
	                        img_url = img_url.split('gifs/detail/', 1)
	                        img_url = img_url[0] + img_url[1]
	                    root, _ = os.path.splitext(img_url)
	                    img_url = root + '-size_restricted.gif'
	                    print ('\nDownloading', subreddit + str(count) + '.gif')
	                    print ('Source:', img_url)
	                    print ('Comments: https://www.reddit.com/r/' + subreddit + '/comments/' + str(
	                        submission))
	                    urllib.urlretrieve(img_url, 'images/%s%i%s' %
	                                       (subreddit, count, '.gif'))
	                    os.remove ('images/%s%i%s' %
	                                           (subreddit, count, '.gif'))
	                    count += 1
	            else:
	                print ('\nCompleted!\n')
	                break

	    except PrawcoreException:
	        print ('\nError accessing subreddit!\n')


        if check==1:
            print(best_match_found)
            sys.stdout.flush()


if __name__ == '__main__':
    arguments = docopt(__doc__)
    main()
