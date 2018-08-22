import json
import requests
import hashlib
import sys

from flask import Flask
from flask import request, make_response, redirect, render_template, url_for, abort, jsonify
app = Flask(__name__)

BLIZZ_API_KEY = 'fj6cra6e62y46crahyxpmf2ky53bn8ks'
AH_URL = ('https://eu.api.battle.net/wow/auction/data/Aerie%20peak?locale=en_GB&apikey='+BLIZZ_API_KEY)
AH_DUMP = None
AH_DUMMP_FILE = 'AH_DUMP.json'
LU_md5 = None


@app.route('/fish')
def api_fish():

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
	#TODO

	if AH_LU != None:
		print ("Updated file")
		print (AH_DUMP)
		return redirect("/fish_prices")
	else:
		return "Not quite"

@app.route('/fish_prices')
def fish_prices():
	vallcore_count = 0
	with open(AH_DUMMP_FILE, 'r') as f:
		ah_json = json.load(f)
		#verify and parse json
		for auc in ah_json['auctions']:
			if auc['owner'] == "Vallcore":
				vallcore_count += 1
		return vallcore_count

	

@app.route("/")
def hello():
		return "WIP"



#Used to create hash
def md5(fname):
	hash = hashlib.md5()
	hash.update(fname)
	return hash

#Starts the server on local network (Forward through router for external access)
if __name__ == "__main__":
	app.debug = True
