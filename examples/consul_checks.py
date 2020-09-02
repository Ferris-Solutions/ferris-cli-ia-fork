import consul
import os
import json


config_key = 'ferris.env'

c = consul.Consul(host=os.environ['CONSUL_HOST'], port=os.environ['CONSUL_PORT'])
index = None

# get a key
index, data = c.kv.get(config_key, index=None)
the_json = data['Value'].decode("utf-8")
config = json.loads(the_json)


# get all keys recursively
index, data = c.kv.get('ferris.apps.dataloader.', recurse=True)
for d in data:
	print(d['Key'])

# any, unknown, passing, warning, or critical

# get services
_, services = c.catalog.services()

for service in services:
	print(service)
	#index, nodes = c.health.service(service)
	index, checks = c.health.checks(service)
	for check in checks:
		print(check['ServiceID'])


states = ['unknown','passing','warning','critical']

for state in states:
	print(f"**** state {state} *****")
	try:
		index, states = c.health.state(state)
		for state in states:
			print(state['ServiceID'])
	except Exception as e:
		pass

#print(data)

#print(config)



   

