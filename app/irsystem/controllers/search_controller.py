from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.accounts.models.user import User
# from app.accounts.model.subreddit_list import Subreddit_List
from flask import request


import pandas as pd
import praw
import json
import time
import numpy as np
from multiprocessing import Process
import sys
import os
import datetime
import requests
from bs4 import BeautifulSoup


project_name = "Reddit Project"
net_id = "Jessica Guo (cg633)"



# get 1245 top subreddit categories:
def get_subreddits():
    '''
    Scrapes redditlist.com for the top 1250 subreddits and then
    drops some of the more offensive/inappropriate subs from the list
    before returning a list of the subs
    '''
    Subreddit_List.delete_all()

    subs = []
    for page in range(1,11):
        req = requests.get('http://redditlist.com/?page={}'.format(page))
        soup = BeautifulSoup(req.text,'lxml')
        top = soup.find_all(class_='span4 listing')[1]
        soup2 = top.find_all(class_='subreddit-url')
        for x in soup2:
            soup3 = x.find_all(class_='sfw')[0].text
            subs.append(soup3)
    #subs that I deemed "undesirable" for my recommender (innapropriate or hostile communities)
    drop_list = ['LadyBoners','Celebs', 'pussypassdenied','MensRights','jesuschristreddit','TheRedPill','NoFap']

    for x in subs:
        if x in drop_list:
            subs.remove(x)
    return subs


@irsystem.route('/get_sub', methods=['GET'])
def get_sub():
	sub_list = get_subreddits()
	for sub in sub_list:
		name = Subreddit_List(subreddit = sub)
		name.insert_self()
	return "Succefully import subreddit titles"







def get_date(created):
    return dt.datetime.fromtimestamp(created)





# @irsystem.route('/', methods=['GET'])
# def start_scraping():
# 	Subreddit.delete_all()

# 	reddit = praw.Reddit(client_id = 'MXTSkv4I47BJuw', 
#                      client_secret='XD5N8cczCsWPnA-VU-qMc-51bO4', 
#                      user_agent='jessicaguo')

# 	# option = request.args.get('sub')
# 	# subreddit = reddit.subreddit(option)
# 	subreddit = reddit.subreddit(announcements)
# 	top_subreddit = subreddit.top(limit=500)

# 	for submission in top_subreddit:
# 		u = Subreddit(title = submission.title, score = submission.score, url = submission.url, 
# 			comments_number = submission.num_comments, post_created_time = dt.datetime.fromtimestamp(submission.created), 
# 			body_text = submission.selftext)
# 		u.insert_self()
# 	return "Succefully import reddit data"
    




@irsystem.route('/', methods=['GET'])
def search():
	sub_li = Subreddit_List.query.all()

	query = request.args.get('search')
	cat = request.args.get('sub')

	

	# option = request.args.get('sub')
	# subreddit = reddit.subreddit(option)
	if cat != None:
		Subreddit.delete_all() # truncate the content of the table
		reddit = praw.Reddit(client_id = 'MXTSkv4I47BJuw', client_secret='XD5N8cczCsWPnA-VU-qMc-51bO4', user_agent='jessicaguo')

		subreddit = reddit.subreddit(cat)
		top_subreddit = subreddit.top(limit=500)

		for submission in top_subreddit:
			u = Subreddit(title = submission.title, score = submission.score, url = submission.url, 
				comments_number = submission.num_comments, post_created_time = dt.datetime.fromtimestamp(submission.created), 
				body_text = submission.selftext)
			u.insert_self()
		
		# username = request.args.get('username')
		# fname = request.args.get('fname')
		# lname = request.args.get('lname')
		# email = request.args.get('email')
		# password = request.args.get('password')
		# if username:
		# 	user = User(fname=fname, lname=lname, email=email, password=password)
		# 	user.insert_self()

		



	if not query:
		data = []
		output_message = ''
	else:

		data = []
		sub_title = Subreddit.query.with_entities(Subreddit.title).all()
		data = list(sub_title)

		# for i in range(10):
		# 	data.append(sub_title[i])

		output_message = "Your search: " + query + ", result num : " + str(query)
		
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data, sub_li = sub_li)

