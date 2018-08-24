import os
import json
import hashlib
import requests

AH_URL = 'https://eu.api.battle.net/wow/auction/data/Aerie%20peak?locale=en_GB&apikey=fj6cra6e62y46crahyxpmf2ky53bn8ks'

def get_ah_db():
	print ("Geting cheapest fish")
    ah_reponse = request.get_json(AH_URL)
    ah_json = ah_reponse.json()

    if ah_json != None:
        lastModified = ah_json['files']['lastModified']
        AH_DUMP_URL = ah_json['files'][0]['url']
        print(lastModified)
        print(AH_DUMP)

    return str(AH_DUMP_URL)


#Run main every 5 mins
def main():
	get_ah_db()

#When lauched call main
if __name__ == "__main__":
	main()