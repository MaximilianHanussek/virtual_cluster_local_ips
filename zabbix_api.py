import os
from pyzabbix.api import ZabbixAPI

# Create ZabbixAPI class instance
zapi = ZabbixAPI(url='http://' + str(os.environ["MASTER_IP_PUBLIC"]) + '/zabbix/', user='Admin', password='zabbix')

# Create new hostgroup
result1 = zapi.do_request('hostgroup.create',
{
	'name': 'Unicore compute nodes'
})

# Get id of newly created hostgroup
parsed_group_id = result1['result']['groupids'][0]

# Get templateid of Linux Template
result2 = zapi.do_request('template.get',
{
	'filter': {'host': ['Template OS Linux']}
})

parsed_template_id = result2['result'][0]['templateid']

# Create new action 
result3 = zapi.do_request('action.create',
{
'name'          : 'Discover new compute nodes'
'esc_period'    : '2m',
'eventsource'   : 2,
'filter'        : {'evaltype': 0,
                   'conditions': [{'conditiontype': 22, 'operator': 2, 'value': 'compute'}]},
                   'operations': [{'operationtype': 4, 'opgroup': [{'groupid': parsed_group_id}]},
                      		 {'operationtype': 6, 'optemplate': [{'templateid': parsed_template_id}]}
				 ]
                  })

# Logout from Zabbix
zapi.user.logout()

