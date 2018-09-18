import os
import json
import requests
import hashlib
import sys
import schedule
import time
import datetime
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
AH_DUMMP_FILE = 'jsonFiles/AH_DUMP.json'
VAL_FILE = 'jsonFiles/item_vals.json'
FISH_VAL_FILE = 'jsonFiles/fish_val.json'
FISH_MIN_VAL_FILE = 'jsonFiles/fish_min.json'
MONITORED_TIEMS = 'jsonFiles/monitored.json'
ACCOUNTS_FILE = 'jsonFiles/accounts.json'

@app.route("/")
@app.route("/index")
@app.route("/index.html")
def home():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        print(session['username'])
	return show_account_listings(session['username'])

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/update_AH')
def update_AH():
	#Get lastest AH listings
	print ("Geting list of fish")
	ah_reponse = requests.get(AH_URL)
	ah_json = ah_reponse.json()
	#Aiisgn json to vars
	AH_LU = ah_json['files'][0]['lastModified']
	AH_DUMP_URL = ah_json['files'][0]['url']
	print(AH_LU)
	print(AH_DUMP_URL)
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
		print ("Updated file")
		print (AH_DUMP)
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
				print(acc)
				return show_account_listings(acc['user'])
		return "Wrong pass"


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
   session.pop('username', None)
   return redirect(url_for('index'))
   
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
	print(request.form['item_id'])
	item_a = request.form['item_id']
	try:
		if not session.get('logged_in'):
			return "You need to be logeed in to use this fool"
		else:
			with open(ACCOUNTS_FILE, mode='r') as acc_json:
				acc_feed = json.load(acc_json)
			for acc in acc_feed['accounts']:
				if acc['user'] == session['username']:
					print['items']
					acc['items'].append(int(item_a))

			with open(ACCOUNTS_FILE, mode='w') as feedsjson:
				json.dump(acc_feed, feedsjson)

			return "added"
	except ValueError:
   		return "That's not an number!"

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

#Get the average price of the fish
@app.route('/fish_avg_val')
def fish_avg_val(fish_id):
	f_count = 0
	avg_price = None
	with open(AH_DUMMP_FILE, 'r') as f:
		ah_json = json.load(f)
		#verify and parse json
		for auc in ah_json['auctions']:
			if auc['item'] == fish_id:
				f_count += 1
				avg_price = fetch_avg_price(auc['item'])
				return avg_price
		return "not listed"
#Get avg price for an item //TODO optional return in gold
def fetch_avg_price(ah_item):
	print("Getting avg price for item")
	i_val = 0
	item_count = 0
	item_list = []
	avg_val_g = float
	with open(AH_DUMMP_FILE, 'r') as f:
		ah_json = json.load(f)
		for auc in ah_json['auctions']:
			if auc['item'] == ah_item:
				item_count += 1
				item_list.append(auc['item'])
				if auc['quantity'] > 1:
					i_val += auc['buyout'] / auc['quantity']
				elif auc['quantity'] == 1:
					i_val += auc['buyout']
	avg_val = (i_val/item_count)
	avg_val_gold = (avg_val/10000)
	return str(avg_val_gold)
#Get the lowest price of item from 
#TODO write this to json file (with max value and date)
def get_min_item_val(item_number):
	print("Getting min price for item")
	i_val = 0
	i_count = 0
	min_price = None
	i_list = []
	with open(AH_DUMMP_FILE, 'r') as f:
		ah_json = json.load(f)
		#verify item exists
		for auc in ah_json['auctions']:
			if auc['item'] == item_number:
				i_count += 1
		print(i_count)
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
				min_price = min(i_list)
				min_price_gold = (min_price/10000)
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
		return redirect("/watched")
	
@app.route('/all_watched')
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
	
	print(session['items'])
	return render_template('watched.html', list_of_items=list_of_items, list_of_names=list_of_names)

def monitored_val_write(a_item):
	avg_val = None
	today = datetime.datetime.now()
	time = today.strftime('%d-%H:%M')
	avg_val = fish_avg_val(a_item)
	min_val = get_min_item_val(a_item)

	print ('['+time+']'+'['+avg_val+']')
	print("Reading file")
	with open(MONITORED_TIEMS, mode='r') as feedsjson:
		feeds = json.load(feedsjson)
	print("Writing to file")
	with open(MONITORED_TIEMS, mode='w') as feedsjson:
		entry = {"item_id":a_item,"avg_val":avg_val,"min_val":min_val,"time":str(time)}
		feeds.append(entry)
		json.dump(feeds, feedsjson)
	return "success"
#####################################
#LEGACY
#####################################
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
	print("ITEM number " + str(item))
	ITEM_URL = ('https://eu.api.battle.net/wow/item/18803?locale=en_GB&jsonp='+str(item)+'&apikey='+BLIZZ_API_KEY)
	item_reponse = requests.get(ITEM_URL)
	item_json = item_reponse.json()
	return item_json


def get_item_name(item):
	print("ITEM number " + str(item))
	ITEM_URL = (ITEM_API+str(item)+'?locale=en_GB&apikey='+BLIZZ_API_KEY)
	item_reponse = requests.get(ITEM_URL)
	#print(ITEM_URL)
	item_json = item_reponse.json()
	#print(item_json)
	return str(item_json['name'])

#Used to create hash
def md5(fname):
	hash = hashlib.md5()
	hash.update(fname)
	return hash

if __name__ == '__main__':
    app.debug = True
    app.run()
