import os
import json
import requests
import hashlib
import sys
import schedule
import time
import datetime
import random, string
from flask import Flask
from flask import request, make_response, redirect, render_template, url_for, abort, jsonify,session,flash
app = Flask(__name__)

AH_DUMP = None
LU_md5 = None

BLIZZ_API_KEY = 'fj6cra6e62y46crahyxpmf2ky53bn8ks'
#Only for Aerie Peak
AH_URL = ('https://eu.api.battle.net/wow/auction/data/Aerie%20peak?locale=en_GB&apikey='+BLIZZ_API_KEY)
ITEM_API = ('https://eu.api.battle.net/wow/item/')
#json files (can never have enough jsons)
#/var/www/AH_Fish/AH_Fish/
AH_DUMMP_FILE = '/var/www/AH_Fish/AH_Fish/jsonFiles/AH_DUMP.json'
VAL_FILE = '/var/www/AH_Fish/AH_Fish/jsonFiles/item_vals.json'
FISH_VAL_FILE = '/var/www/AH_Fish/AH_Fish/jsonFiles/fish_val.json'
FISH_MIN_VAL_FILE = '/var/www/AH_Fish/AH_Fish/jsonFiles/fish_min.json'
MONITORED_TIEMS = '/var/www/AH_Fish/AH_Fish/jsonFiles/monitored.json'
ACCOUNTS_FILE = '/var/www/AH_Fish/AH_Fish/jsonFiles/accounts.json'
NOTIFICATIONS_FILE = '/var/www/AH_Fish/AH_Fish/jsonFiles/notifications.json'
ITEM_NAMES_FILE = '/var/www/AH_Fish/AH_Fish/jsonFiles/item_names.json'

@app.route("/")
@app.route("/index")
@app.route("/index.html")
@app.route("/index.php")
def home():
	if not session.get('logged_in'):
		return render_template('index.html')
	return show_account_listings(session['username'])

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/update_AH')
def update_AH():
	#Get lastest AH listings
	print ("Downloading latest AH")
	ah_reponse = requests.get(AH_URL)
	ah_json = ah_reponse.json()
	#Aiisgn json to vars
	AH_LU = ah_json['files'][0]['lastModified']
	AH_DUMP_URL = ah_json['files'][0]['url']
	#Check if the last updated time has changed before redownloading listings
	new_md5 = md5(str(AH_LU))
	if LU_md5 == None or new_md5 != AH_LU:
		AH_LU = str(new_md5)
		#Get AH listings
		ah_dump_reponse = requests.get(AH_DUMP_URL)
		ah_dump_json = ah_dump_reponse.json()
		#Dump it into a json file
		with open(AH_DUMMP_FILE, 'w') as f:
			json.dump(ah_dump_json, f)
		print("Updaing JSON AH file")
	#redirect to page to pass
	if AH_LU != None:
		print ("Latest AH downloaded")
		return render_template('index.html')
	else:
		return "Not quite"

#########################
#Login 
#########################
app.secret_key = os.urandom(12)
@app.route('/login')
def login():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return "Hello Boss!"

@app.route('/verifylogin', methods=['POST'])
def do_admin_login():
	request_user_pass = request.form['password']
	request_user = request.form['username']
	with open(ACCOUNTS_FILE, mode='r') as f:
		feeds = json.load(f)
		for acc in feeds['accounts']:					
			if str(request_user_pass) == str(acc['pass']) and str(request_user) == str(acc['user']):
				session['logged_in'] = True
				print("logging in")
				session['username'] = acc['user']
				load_session_data(session['username'])
				return show_account_listings(acc['user'])
		return "Wrong pass"

def load_session_data(account_name):
	#Load notifications
	count_of_notifications = 0
	account_notifications = []
	account_watched_items = []
	account_watched_items_names ={}
	with open(NOTIFICATIONS_FILE, mode='r') as noti_feed:
		noti_json = json.load(noti_feed)
		for noti in noti_json:
			if noti['user_id'] == account_name:
				if noti['read'] == 0:
					count_of_notifications += 1
					account_notifications.append(noti)
		session['notification_dics'] = account_notifications
		session['notification_count'] = count_of_notifications
	with open(ACCOUNTS_FILE, mode='r') as acc_json:
		feed_a = json.load(acc_json)
		for acc in feed_a['accounts']:
			if acc['items'] > 0:
				if acc['user'] == account_name:
					for item in acc['items']:
						account_watched_items.append(item)
						account_watched_items_names[item] = get_item_name(item)
		session['account_watched_items'] = account_watched_items
		session['account_watched_items_names'] = account_watched_items_names

def show_account_listings(account):
	list_of_items = []
	list_of_names = {}
	with open(ACCOUNTS_FILE, mode='r') as acc_json:
		feed_a = json.load(acc_json)
		for acc in feed_a['accounts']:
			if acc['items'] > 0:
				if acc['user'] == account:
					for item in acc['items']:
						list_of_items.append(item)
						list_of_names[item] = get_item_name(item)
						session['items'] = list_of_items
	#print(str(list_of_items))
	return render_template('watched.html', list_of_items=list_of_items, list_of_names=list_of_names)

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   #session.pop('username', None)
   session['logged_in'] = False
   return home()

#########################
#Load account page
#########################
@app.route('/account')
def account():
	if session.get('logged_in'):
		#reload session data
		load_session_data(session['username'])
		return render_template('account.html')
	else:
		return "You need to be logged in to view this"


#########################
#Mark notifications as read
#########################
@app.route('/mark_item_read', methods=['GET', 'POST'])
def mark_item_read():
	form_item = request.form['notification_id']
	user_id = request.form['user_id']
	with open(NOTIFICATIONS_FILE, mode='r') as feedsjson:
		noti_json = json.load(feedsjson)
	for n_item in noti_json:
		if n_item['notification_id'] == form_item:
			if n_item['user_id'] == user_id:
				n_item['read'] = 1
	with open(NOTIFICATIONS_FILE, mode='w') as feedsjson:
		json.dump(noti_json, feedsjson)
	#reload session data
	load_session_data(user_id)
	return account()
  

#########################
#JSON endponts
#########################
#Load local avg json file
@app.route('/fish_avg.json')
def fish_avg():
	with open(FISH_VAL_FILE, mode='r') as a_json:
		feed_a = json.load(a_json)
	return jsonify(feed_a)

#Load local json file
@app.route('/fish_min.json')
def fish_min():
	with open(FISH_MIN_VAL_FILE, mode='r') as m_json:
		feed_f = json.load(m_json)
	return jsonify(feed_f)

#Load local json file
@app.route('/monitored.json')
def monitored():
	with open(MONITORED_TIEMS, mode='r') as m_json:
		feed_f = json.load(m_json)
	return jsonify(feed_f)	

@app.route('/find_user', methods=['GET', 'POST'])
def find_user():
	#parse username
	name = request.form['search_name']
	listing = search_username(name)
	return str(listing)

#########################
#Updating account watch lists
#########################

@app.route('/add_item', methods=['POST'])
def add_item():
	item_a = request.form['item_id']
	try:
		if not session.get('logged_in'):
			return "You need to be logeed in to use this fool"
		else:
			with open(ACCOUNTS_FILE, mode='r') as acc_json:
				acc_feed = json.load(acc_json)
			for acc in acc_feed['accounts']:
				if acc['user'] == session['username']:
					for a_item in acc['items']:
						if int(item_a) == int(a_item):
							return "You cannot add something you are already watching silly"
					acc['items'].append(int(item_a))

			with open(ACCOUNTS_FILE, mode='w') as feedsjson:
				json.dump(acc_feed, feedsjson)
			return account()
	except ValueError:
   		return "That's not an number!"

#########################
#Adding all items to an account
#########################

@app.route('/add_item_all_items')
def add_item_all_items():
	try:
		if not session.get('logged_in'):
			return "You need to be logeed in to use this fool"
		else:	
			with open(ACCOUNTS_FILE, mode='r') as acc_json:
				acc_feed = json.load(acc_json)
			for acc in acc_feed['accounts']:
				if acc['user'] == session['username']:
					with open(AH_DUMMP_FILE, 'r') as f:
						ah_json = json.load(f)
					for auc in ah_json['auctions']:
						account_watched_count = 0
						for account_wated in acc['items']:
							if account_wated == auc['item']:
								account_watched_count += 1
						if account_watched_count == 0:
							print("Adding item "+ str(auc['item']))
							acc['items'].append(auc['item'])
					
			with open(ACCOUNTS_FILE, mode='w') as feedsjson:
				json.dump(acc_feed, feedsjson)
			return account()
	except ValueError:
   		return "That's not an number!"

#########################
#Remove items from watched in acocunt
#########################

@app.route('/remove_item', methods=['POST'])
def remove_item():
	item_r = request.form['item_id']
	try:
		if not session.get('logged_in'):
			return "You need to be logeed in to use this fool"
		else:
			with open(ACCOUNTS_FILE, mode='r') as acc_json:
				acc_feed = json.load(acc_json)
			for acc in acc_feed['accounts']:
				if acc['user'] == session['username']:
					acc['items'].remove(int(item_r))
					print("Removing item "+str(item_r)+" from acc "+str(session['username']))
					#acc['items'].pop(int(item_r))

			with open(ACCOUNTS_FILE, mode='w') as feedsjson:
				json.dump(acc_feed, feedsjson)

			return account()
	except ValueError:
   		return "That's not an number!"

#########################
#Generating notifications for accounts
#########################

def does_it_need_notification(item, avg_value, min_value):
	if avg_value == "not listed":
		avg_value = 0
	elif min_value == "not listed":
		min_value = 0
	item_name = get_item_name(item)
	#Average the value for the last week
	item_list = []
	print("Checking if item "+ str(item)+" needs a notification")
	with open(MONITORED_TIEMS, mode='r') as feedsjson:
		mon_json = json.load(feedsjson)
		for m_item in mon_json:
			if m_item['item_id'] == item:
				if m_item['avg_val'] != "not listed":
					if len(item_list) > 10:
						item_list.pop(0)
					else:
						item_list.append(int(m_item['avg_val']))
	if len(item_list) != 0:
		week_avg = sum(item_list) / len(item_list)
	else:
		week_avg = int(avg_value)
	#check if the min_value is 20%/30% less than avg of past week
	val_change = abs(week_avg-int(min_value))
	per_change = get_change(val_change,week_avg)

	#Get all accounts with this ID
	list_accounts_with_item = []
	with open(ACCOUNTS_FILE, mode='r') as acc_feed:
		acc_json = json.load(acc_feed)
		for acc in acc_json['accounts']:
			if acc['items'] > 0:
				for acc_item in acc['items']:
					if acc_item == item:
						if acc['user'] not in list_accounts_with_item:
							list_accounts_with_item.append(acc['user'])
	#Write data to notifications file
	with open(NOTIFICATIONS_FILE, mode='r') as noti_feed:
		noti_json = json.load(noti_feed)
	today = datetime.datetime.now()
	time = today.strftime('%x-%X')

	#Create notification if value is greater than 10
	if per_change > 10 and per_change < 30:
		#create notification for account
		for account in list_accounts_with_item:
			existing_notificaiton = 0
			#Generate random string for an id for each notificaiton
			noti_to_hash = (str(account)+str(item)+str(per_change))
			hash_of_noti = md5hex(noti_to_hash)
			noti_id = hash_of_noti
			#Check if item has already been added
			existing_notificaiton = check_noti_for_acc(account, item)
			if existing_notificaiton != 0:
				#Update existing notification
				print("Updating existing notification")
				update_noti_for_acc(account, existing_notificaiton,per_change,"green",item)
			else:
				#Generate new notificaiton
				print("Creating new notification")
				entry = {"notification_id":noti_id,  "user_id":account,"item_id":item,"item_name":item_name,  "value_diff":val_change,"percent_diff":per_change, "read":0,"created":time, "category":"green"}
				noti_json.append(entry)		

	elif per_change > 30 and per_change < 50:
		for account in list_accounts_with_item:
			existing_notificaiton = 0
			#Generate random string for an id for each notificaiton
			noti_to_hash = (str(account)+str(item)+str(per_change))
			hash_of_noti = md5hex(noti_to_hash)
			noti_id = hash_of_noti
			#Check if item has already been added
			existing_notificaiton = check_noti_for_acc(account, item)
			if existing_notificaiton != 0:
				#Update existing notification
				print("Updating existing notification")
				update_noti_for_acc(account, existing_notificaiton,per_change,"orange",item)
			else:
				#Generate new notificaiton
				print("Creating new notification")
				entry = {"notification_id":noti_id,  "user_id":account,"item_id":item,"item_name":item_name,  "value_diff":val_change,"percent_diff":per_change, "read":0,"created":time, "category":"orange"}
				noti_json.append(entry)
				
	elif per_change > 50:
		for account in list_accounts_with_item:
			existing_notificaiton = 0
			#Generate random string for an id for each notificaiton
			noti_to_hash = (str(account)+str(item)+str(per_change))
			hash_of_noti = md5hex(noti_to_hash)
			noti_id = hash_of_noti
			#Check if item has already been added
			existing_notificaiton = check_noti_for_acc(account, item)
			if existing_notificaiton != 0:
				#Update existing notification
				print("Updating existing notification")
				update_noti_for_acc(account, existing_notificaiton,per_change,"red",item)
			else:
				#Generate new notificaiton
				print("Creating new notification")
				entry = {"notification_id":noti_id,  "user_id":account,"item_id":item,"item_name":item_name,  "value_diff":val_change,"percent_diff":per_change, "read":0,"created":time, "category":"red"}
				noti_json.append(entry)


	with open(NOTIFICATIONS_FILE, mode='w') as feedsjson:
		json.dump(noti_json, feedsjson)

def randomstring(length):
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(length))

def check_noti_for_acc(account_name, item_id):
	with open(NOTIFICATIONS_FILE, mode='r') as noti_feed:
		noti_json = json.load(noti_feed)
	for n_item in noti_json:
		if n_item['user_id'] == account_name:
			if n_item['item_id'] == item_id:
				return n_item['notification_id']
	return 0

def update_noti_for_acc(account_name, notification_id, new_val,color,item_id):
	with open(NOTIFICATIONS_FILE, mode='r') as noti_feed:
		noti_json = json.load(noti_feed)
	#noti_to_hash = (str(account_name)+str(item_id)+str(new_val))
	#hash_of_noti = md5hex(noti_to_hash)
	#noti_id = hash_of_noti
	today = datetime.datetime.now()
	time = today.strftime('%x-%X')
	for n_item in noti_json:
		if n_item['user_id'] == account_name:
			if n_item['notification_id'] == notification_id:
				if n_item['percent_diff'] != new_val:
					n_item['category'] = color
					n_item['read'] = 0
					n_item['percent_diff'] = new_val
					n_item['created'] = time

	with open(NOTIFICATIONS_FILE, mode='w') as feedsjson:
		json.dump(noti_json, feedsjson)

#Used to get percentage value
def get_change(current, previous):
    if current == previous:
        return 100.0
    try:
        return round((float(current) / previous * 100.0),1)
    except ZeroDivisionError:
        return 0

#########################
#Pull prices for items from AH_DUMP
#########################

#Get avg price for an item //TODO optional return in gold
def get_avg_price(item_number):
	print("Getting avg price for item " +str(item_number))
	new_item_val = 0
	i_val = 0
	item_count = 0
	with open(AH_DUMMP_FILE, 'r') as f:
		ah_json = json.load(f)
		for auc in ah_json['auctions']:
			if auc['item'] == item_number:
				if auc['buyout'] != 0:
					item_count += 1
					new_item_val = auc['buyout']
					if auc['quantity'] > 1:
							i_val += (auc['buyout'] / auc['quantity'])
					elif auc['quantity'] == 1:
							i_val += auc['buyout']
	if i_val != 0:
		avg_val = (i_val/item_count)
		avg_val_gold = (avg_val/10000)
	elif i_val == 0:
		avg_val = new_item_val
		avg_val_gold = new_item_val
	return str(avg_val_gold)
#Get the lowest price of item from 
#TODO write this to json file (with max value and date)
def get_min_item_val(item_number):
	print("Getting min price for item "+str(item_number))
	i_val = 0
	i_count = 0
	min_price = None
	i_list = []
	list_items = 0
	with open(AH_DUMMP_FILE, 'r') as f:
		ah_json = json.load(f)
		#verify item exists
		for auc in ah_json['auctions']:
			if auc['item'] == item_number:
				i_count += 1
		if i_count >= 1:
			#Search through file for lowest value
			with open(AH_DUMMP_FILE, 'r') as f:
				ah_json = json.load(f)
				for auc in ah_json['auctions']:
					if auc['item'] == item_number:
						if auc['quantity'] > 1:
							if auc['buyout'] != 0:
								i_val = auc['buyout'] / auc['quantity']
								i_list.append(i_val)
						elif auc['quantity'] == 1:
							if auc['buyout'] != 0:
								i_val = auc['buyout']
								i_list.append(i_val)
				for list_item in i_list:
					list_items +=1
				if list_items != 0:
					min_price = min(i_list)
					min_price_gold = (min_price/10000)
				else:
					min_price_gold = 0
			return str(min_price_gold)
		else:
			return "not listed"

@app.route('/write_monitored_values')
def write_monitored_values():
	with open(ACCOUNTS_FILE, mode='r') as acc_json:
		feed_a = json.load(acc_json)
		for acc in feed_a['accounts']:
			if acc['items'] > 0:
				for item in acc['items']:
					print("Adding item " + str(item))
					monitored_val_write(item)
			else:
				return "No monitored items"
		return home()
	
@app.route('/watched')
def watched():
	list_of_items = []
	list_of_names = {}
	with open(ACCOUNTS_FILE, mode='r') as acc_json:
		feed_a = json.load(acc_json)
		for acc in feed_a['accounts']:
			if acc['items'] > 0:
				for item in acc['items']:
					list_of_items.append(item)
					list_of_names[item] = get_item_name(item)
	#print(str(list_of_names))
	return render_template('watched.html', list_of_items=list_of_items, list_of_names=list_of_names)

def monitored_val_write(a_item):
	today = datetime.datetime.now()
	time = today.strftime('%d-%H:%M')
	avg_val = get_avg_price(a_item)
	min_val = get_min_item_val(a_item)
	does_it_need_notification(a_item,avg_val,min_val)
	print("Reading MONITORED_TIEMS")
	with open(MONITORED_TIEMS, mode='r') as feedsjson:
		feeds = json.load(feedsjson)
	print("Writing item to MONITORED_TIEMS")
	with open(MONITORED_TIEMS, mode='w') as feedsjson:
		entry = {"item_id":a_item,"avg_val":avg_val,"min_val":min_val,"time":time}
		feeds.append(entry)
		json.dump(feeds, feedsjson)
	return "success"


#####################################
#LEGACY
#####################################

#Count number of fish (needs to be changes to it can be passed an ID)
@app.route('/fish_count')
def fish_count():
	f_count = 0
	with open(AH_DUMMP_FILE, 'r') as f:
		ah_json = json.load(f)
		#verify and parse json
		for auc in ah_json['auctions']:
			#Item is Savory Delight
			if auc['item'] == 6657:
				f_count += 1
				print (auc['item'])
	return str(f_count)

#TODO read in file of monitored items
@app.route('/fish_monitored_values_write')
def fish_monitored_values_write():
	monitored_items = 6657
	fish_avg_val_write(monitored_items)
	fish_min_val_write(monitored_items)
	return render_template('index.html')	

def fish_avg_val_write(a_item):
	avg_val = None
	today = datetime.datetime.now()
	time = today.strftime('%d-%I%p')
	#Item is currently Savory Delights
	avg_val = fish_avg_val(a_item)
	print ('['+time+']'+'['+avg_val+']')
	print("Reading file")
	with open(FISH_VAL_FILE, mode='r') as feedsjson:
		feeds = json.load(feedsjson)
	print("Writing to file")
	with open(FISH_VAL_FILE, mode='w') as feedsjson:
		entry = {"item_id":a_item,"val":avg_val, "time":str(time)}
		feeds.append(entry)
		json.dump(feeds, feedsjson)
	return "success"
	
def fish_min_val_write(m_item):
	min_val = None
	today = datetime.datetime.now()
	time = today.strftime('%d-%I%p')
	#Item is currently Savory Delights
	min_val = get_min_item_val(m_item)
	print ('['+time+']'+'['+min_val+']')
	print("Reading file")
	with open(FISH_MIN_VAL_FILE, mode='r') as feedsjson:
		feeds = json.load(feedsjson)
	print("Writing to file")
	with open(FISH_MIN_VAL_FILE, mode='w') as feedsjson:
		entry = {"item_id":m_item,"val":min_val, "time":str(time)}
		feeds.append(entry)
		json.dump(feeds, feedsjson)
	return "success"
#Legacy
@app.route('/fish_avg_val_write')
def write_avg_fish_val():
	avg_val = None
	today = datetime.datetime.now()
	time = today.strftime('%d-%I%p')
	#Item is currently Savory Delights
	avg_val = fish_avg_val(6657)
	print ('['+time+']'+'['+avg_val+']')
	print("Reading file")
	with open(FISH_VAL_FILE, mode='r') as feedsjson:
		feeds = json.load(feedsjson)
	print("Writing to file")
	with open(FISH_VAL_FILE, mode='w') as feedsjson:
		entry = {"name":"Savory Delights", "val":avg_val, "time":str(time)}
		feeds.append(entry)
		json.dump(feeds, feedsjson)
	return "success"

#Load local json file
@app.route('/test.json')
def test_json():
	with open(FISH_VAL_FILE, mode='r') as feedsjson:
		feeds = json.load(feedsjson)
	return jsonify(feeds)


#Seach users and build list of their listed items
def search_username(uname):
	uname_count =0 
	AH_items = []
	User_Iist_Item_details = []
	Listed_Items = []
	with open(AH_DUMMP_FILE, 'r') as f:
		ah_json = json.load(f)
		#verify and parse json
		for auc in ah_json['auctions']:
			if auc['owner'] == uname:
				uname_count += 1
				AH_items.append(auc['owner'])
				#AH_items.append(auc['item'])
				#AH_items.append(auc['buyout'])
				#User_Iist_Item_details.append(auc['item'])
				#AH_items.append(auc['ownerRealm'])	
#		for i in User_Iist_Item_details:
#			Listed_Items.append(get_item_details(i))
		if uname_count != 0: 
			return AH_items	
		else:
			return "No users with that name current on AH" 

#Get json dic of from item number and return json item
def get_item_details(item):
	print("Getting item number " + str(item))
	ITEM_URL = ('https://eu.api.battle.net/wow/item/18803?locale=en_GB&jsonp='+str(item)+'&apikey='+BLIZZ_API_KEY)
	item_reponse = requests.get(ITEM_URL)
	item_json = item_reponse.json()
	return item_json


def get_item_name(item):
	with open(ITEM_NAMES_FILE, mode='r') as item_feed:
		items_json = json.load(item_feed)
	num_of_items = 0
	for items in items_json:
		if items['item_id'] == item:
			num_of_items +=1
			print("Getting item name " + str(item))
			return items['item_name']

	if num_of_items == 0:
		print("Getting item name using api call " + str(item))
		ITEM_URL = (ITEM_API+str(item)+'?locale=en_GB&apikey='+BLIZZ_API_KEY)
		item_reponse = requests.get(ITEM_URL)
		item_json = item_reponse.json()
		with open(ITEM_NAMES_FILE, mode='w') as item_feed:
			try:
				item_utf8 = item_json['name']
				entry = {"item_id":item, "item_name":item_utf8.encode('utf-8')}
				items_json.append(entry)
			except:
				item_utf8 = "Unable to read name"
				entry = {"item_id":item, "item_name":"Unable to read name"}
				items_json.append(entry)
			json.dump(items_json, item_feed)
		return item_utf8.encode('utf-8')

#Used to create hash
def md5(fname):
	hash = hashlib.md5()
	hash.update(fname)
	return hash

def md5hex(w):
    return hashlib.md5(w).hexdigest()[:9]

if __name__ == '__main__':
    app.debug = True
    app.run(host= '0.0.0.0')
