from neo.libs import login as login_lib
from neutronclient.v2_0 import client as neutron_client


def get_neutron_client(session=None):
    if not session:
        session = login_lib.load_dumped_session()
    neutron = neutron_client.Client(session=session)
    return neutron


def get_list(session=None):
    neutron = get_neutron_client(session)
    networks = neutron.list_networks()
    return networks['networks']


def get_floatingips(session=None):
    neutron = get_neutron_client(session)
    floatingips = neutron.list_floatingips()
    return floatingips['floatingips']


def do_delete(network_id, session=None):
    neutron = get_neutron_client(session)
    neutron.delete_network(network_id)


def list_sec_group(session=None):
    neutron = get_neutron_client(session)
    sec_group =  neutron.list_security_groups()
    return sec_group['security_groups']


def rules_sec_groups(sec_group, session=None):
    obj_sec_rule = list()
    neutron = get_neutron_client(session)
    sec_group =  neutron.list_security_groups()
    sec_group = sec_group['security_groups']
    for i in sec_group:
        data = {
            'name': i['name'],
            'description': i['description']
        }
        obj_sec_rule.append(data)
    return obj_sec_rule
