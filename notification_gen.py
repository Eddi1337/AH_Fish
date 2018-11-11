def write_monitored_values():
	listings = []
	with open(ACCOUNTS_FILE, mode='r') as acc_json:
		feed_a = json.load(acc_json)
		for acc in feed_a['accounts']:
			if acc['items'] > 0:
				for item in acc['items']:
					if item in listings:
						print("Item " + str(item) + " already watched")
					else:
						monitored_val_write(item)	
						print("Adding item to list" + str(item))
						listings.append(item)
					
			else:
				return "No monitored items"
		print("Pulled monitored values for items: " + str(listings))
		return home()


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



