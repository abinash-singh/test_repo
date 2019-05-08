def obj_to_list(obj):
	temp = []

	for i in obj:
		transaction_id = i.get('transaction_id')
		utc_timestamp = i.get('utc_timestamp')
		primary_id_file = i.get('primary_id_file')
		auth_key = i.get('auth_key')
		name = i.get('name')
		phone_number = i.get('phone_number')

		temp.append({'transaction_id' :  transaction_id, 'utc_timestamp' :  utc_timestamp, 'primary_id_file' : primary_id_file, 'auth_key': auth_key, 'name' : name, 'phone_number' : phone_number})
	return temp