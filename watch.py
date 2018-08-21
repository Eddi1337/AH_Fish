import json
import requests
from flask import Flask
from flask import request, make_response, redirect, render_template, url_for, abort, jsonify
app = Flask(__name__)

BLIZZ_API_KEY = 'fj6cra6e62y46crahyxpmf2ky53bn8ks'
AH_URL = 'https://eu.api.battle.net/wow/auction/data/Aerie%20peak?locale=en_GB&apikey=fj6cra6e62y46crahyxpmf2ky53bn8ks'
AH_DUMP = None
AH_DUMMP_FILE = 'AH_DUMP.dump'


@app.route('/fish')
def api_fish():
    print ("Geting cheapest fish")
    ah_reponse = request.get_json(AH_URL)
    print("Writing reponse to file") 
    print(ah_reponse)


    if AH_DUMP != None:
        print ("Getting data")
        print (AH_DUMP)

    else:
        print ("No data returned")


@app.route("/")
def hello():
        return "Hello World!"
